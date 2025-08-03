self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

def on_tab_selected(self, event):
    selected_tab = event.widget.select()
    tab_index = event.widget.index(selected_tab)
    tab_name = self.notebook.tab(selected_tab, "text")

    if tab_name == "History":
        print("History tab selected")
        self.refresh_history()
    elif tab_name == "Main":
        print("Main tab selected")
        self.refresh_items()
    elif tab_name == "Chart":
        print("Chart tab selected")
        # self.update_chart()  ← if you add such a method
    elif tab_name == "Graph":
        print("Graph tab selected")
        # self.update_graph()  ← if you add such a method
