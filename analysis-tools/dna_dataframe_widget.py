import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output


class OrganismGradeViewer:
    def __init__(self, dataframe:pd.DataFrame, unique_column:str, ranking_column:str, useful_cols:list[str], dropna_for_unique:bool=True):
        self.unique_column_as_series =  dataframe[unique_column].value_counts(normalize=False,dropna=dropna_for_unique)
        self.unique_column_title = unique_column
        self.ranking_column_title = ranking_column

        # I can't rank it/group it if the unique_col and ranking_col are not in the dataframe's useful columns
        if unique_column not in useful_cols:
            useful_cols.append(unique_column)
        if ranking_column not in useful_cols:
            useful_cols.append(ranking_column)

        self.useful_columns = dataframe[useful_cols]

        # Input widgets
        self._input_widget_builder()

        # Output widget
        self.output_widget = widgets.Output(layout={'border': '1px solid black'})


    def _input_widget_builder(self):
        # Widgets
        self.column_pick_input = widgets.Dropdown(
            options=list(self.unique_column_as_series.index),
            value=self.unique_percent.index[0],
            description=f'{self.unique_column_title}:',
            disabled=False,
            continuous_update=False
        )

        self.num_results_input = widgets.BoundedIntText(
            value=3,
            min=1,
            max=self.unique_column_as_series.loc(self.column_pick_input.value),
            step=1,
            description=f'Ordered by {self.ranking_column_title}:',
            disabled=False,
            continuous_update=False
        )

        self.ascending_input = widgets.Checkbox(
            value=False,
            description='Ascending Grade Order',
            disabled=False,
            continuous_update=False
        )

    def display(self):
        # Display inputs
        self.column_pick_input.observe(self._on_change, names='value')
        self.num_results_input.observe(self._on_change, names='value')
        self.ascending_input.observe(self._on_change, names='value')
        # Initial display of outputs
        self._update_output()
        display(self.column_pick_input, self.num_results_input, self.ascending_input, self.output_widget)

    def _update_output(self):
        with self.output_widget:
            clear_output()
            self._show_top_hits(
                self.column_pick_input.value,
                self.num_results_input.value,
                self.ascending_input.value
            )

    def _show_top_hits(self, selected_value, n_results, ascending):
        filtered = self.useful_columns[self.useful_columns[self.unique_column_title] == selected_value]
        filtered = filtered.sort_values(self.ranking_column_title, ascending=ascending)
        display(filtered.loc[:, self.useful_columns].head(n_results))

    def _on_change(self, change):
        self._update_output()

    

def main():
    pass

if __name__ == "__main__":
    main()