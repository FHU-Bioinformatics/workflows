#!/bin/bash

# ===========================================
# Restore Proxmox VM from .vma.zst backup
# ===========================================
# Usage:
#   ./restore_raw_vm.sh <vma.zst file> <vmid|auto> <storage> [--ram <GB>] [--cpu <cores>] [--name <vm-name>]
#
# Example:
#   ./restore_raw_vm.sh vzdump-qemu-101.vma.zst auto local-lvm --name myvm
# ===========================================

set -e

# -------------------------------
# Defaults
# -------------------------------
RAM_GB=8
CORES=4
VM_NAME=""
DEFAULT_START_ID=100

usage() {
    echo "Usage: $0 <vma.zst file> <vmid|auto> <storage> [--ram <GB>] [--cpu <cores>] [--name <vm-name>]"
    echo
    echo "  --ram     RAM in GB (default: 8)"
    echo "  --cpu     CPU cores (default: 4)"
    echo "  --name    VM name (default: imported-<vmid>)"
    echo "  -h, --help Show this help"
    exit 1
}

# -------------------------------
# Parse Positional Args
# -------------------------------
if [[ "$#" -lt 3 ]]; then
    usage
fi

VMA_ZST="$1"
VMID_RAW="$2"
STORAGE="$3"
shift 3

# -------------------------------
# Parse Flags
# -------------------------------
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --ram)
            RAM_GB="$2"
            shift 2
            ;;
        --cpu)
            CORES="$2"
            shift 2
            ;;
        --name)
            VM_NAME="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "❌ Unknown option: $1"
            usage
            ;;
    esac
done

# -------------------------------
# Auto-pick VM ID if "auto"
# -------------------------------
if [[ "$VMID_RAW" == "auto" ]]; then
    echo "🔍 Finding next available VM ID..."
    USED_IDS=$(qm list | awk 'NR>1 {print $1}')
    NEW_VM_ID=$DEFAULT_START_ID
    while echo "$USED_IDS" | grep -q "^$NEW_VM_ID$"; do
        ((NEW_VM_ID++))
    done
    echo "✅ Chose unused VM ID: $NEW_VM_ID"
else
    NEW_VM_ID="$VMID_RAW"
fi

[[ -z "$VM_NAME" ]] && VM_NAME="imported-${NEW_VM_ID}"
RAM_MB=$((RAM_GB * 1024))
BASENAME=$(basename "$VMA_ZST" .vma.zst)
VMA="${BASENAME}.vma"
EXTRACT_DIR="/var/tmp/${BASENAME}"

# -------------------------------
# 📦 Decompress the VMA.ZST
# -------------------------------
echo "📦 Decompressing $VMA_ZST..."
zstd -d -f "$VMA_ZST" -o "$VMA"

# -------------------------------
# 📂 Extract the VMA Archive
# -------------------------------
echo "📂 Extracting VMA to $EXTRACT_DIR..."
mkdir -p "$EXTRACT_DIR"
vma extract "$VMA" "$EXTRACT_DIR"

RAW_DISK=$(find "$EXTRACT_DIR" -name '*.raw' | head -n 1)
if [[ -z "$RAW_DISK" ]]; then
    echo "❌ No raw disk image found."
    exit 2
fi

# -------------------------------
# 🖥️ Create the VM
# -------------------------------
echo "🆕 Creating VM $NEW_VM_ID named \"$VM_NAME\" with $CORES cores, $RAM_MB MB RAM..."
qm create "$NEW_VM_ID" \
    --name "$VM_NAME" \
    --memory "$RAM_MB" \
    --cores "$CORES" \
    --net0 virtio,bridge=vmbr0

# -------------------------------
# 📤 Import the Disk
# -------------------------------
echo "📤 Importing raw disk..."
qm importdisk "$NEW_VM_ID" "$RAW_DISK" "$STORAGE"

echo "🔗 Attaching disk to VM..."
qm set "$NEW_VM_ID" --scsihw virtio-scsi-pci --scsi0 "${STORAGE}:vm-${NEW_VM_ID}-disk-0"
echo "🔗 Setting boot order..."
qm set "$NEW_VM_ID" --boot order=scsi0


# -------------------------------
# ▶️ Start the VM
# -------------------------------
echo "▶️ Starting VM $NEW_VM_ID..."
qm start "$NEW_VM_ID"

# -------------------------------
# 🧹 Cleanup
# -------------------------------
echo "🧹 Cleaning up..."
rm -f "$VMA"
rm -rf "$EXTRACT_DIR"

echo "✅ VM $NEW_VM_ID ('$VM_NAME') is running. All done."
