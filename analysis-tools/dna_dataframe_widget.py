import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output

class OrganismGradeViewer:
    def __init__(self, clean_hits, organism_percent, useful_cols):
        self.clean_hits = clean_hits
        self.organism_percent = organism_percent
        self.useful_cols = useful_cols

        # Output widget
        self.output_organism = widgets.Output(layout={'border': '1px solid black'})

        # Widgets
        self.organism_dropdown = widgets.Dropdown(
            options=list(self.organism_percent.index),
            value=self.organism_percent.index[0],
            description='Organism:',
            disabled=False,
            continuous_update=False
        )

        self.num_results_input = widgets.BoundedIntText(
            value=3,
            min=1,
            max=len(self.clean_hits),
            step=1,
            description='Top Grade #:',
            disabled=False,
            continuous_update=False
        )

        self.ascending_input = widgets.Checkbox(
            value=False,
            description='Ascending Grade Order',
            disabled=False,
            continuous_update=False
        )

        # Bind events
        self.organism_dropdown.observe(self._on_change, names='value')
        self.num_results_input.observe(self._on_change, names='value')
        self.ascending_input.observe(self._on_change, names='value')

        # Initial display
        self._update_output()

    def _show_top_hits(self, organism_name, n_results, ascending):
        filtered = self.clean_hits[self.clean_hits['Organism'] == organism_name]
        try:
            filtered = filtered.copy()
            filtered['Grade_numeric'] = filtered['Grade'].str.rstrip('%').astype(float)
            filtered = filtered.sort_values('Grade_numeric', ascending=ascending)
        except Exception:
            filtered = filtered.sort_values('Grade', ascending=ascending)
        display(filtered.loc[:, self.useful_cols].head(n_results))

    def _on_change(self, change):
        self._update_output()

    def _update_output(self):
        with self.output_organism:
            clear_output()
            self._show_top_hits(
                self.organism_dropdown.value,
                self.num_results_input.value,
                self.ascending_input.value
            )

    def display(self):
        display(self.organism_dropdown, self.num_results_input, self.ascending_input, self.output_organism)


def main():
    pass

if __name__ == "__main__":
    main()