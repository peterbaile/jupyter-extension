define([
    'base/js/namespace',
    'base/js/events',
    'jquery',
    'base/js/utils'
], function (
    Jupyter,
    events,
    $,
    utils
) {

    const getCookie = (name) => {
        const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    };

    // Add a cell above current cell (will be top if no cells)
    const add_cell = () => {
        Jupyter.notebook.insert_cell_above('code').// Define default cell here
        set_text(`# Standard data science libraries
import pandas as pd
import numpy as np
from scipy import stats
import featuretools as ft
# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('bmh')
# Options for pandas
pd.options.display.max_columns = 20
# Display all cell outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
        `);

        const send_url = utils.url_path_join(Jupyter.notebook.base_url, '/juneau-2');

        const data_json = {'var': 'df', "_xsrf": getCookie("_xsrf")};

        $.ajax({
            url: send_url,
            method: 'PUT',
            data: data_json,
            dataType: 'json',
            timeout: 10000000,
            success: function(response) {
                alert("Success!");
                console.log("success! juneau-2")
                // return_state = response['state'];
                // return_data = response['res'];
                // if (return_state === 'true') {
                //     var print_string = return_data.toString();
                // } else {
                //     alert("Error indexing table!");
                // }
            },
            error: function (request, error) {
                // console.log(arguments);
                alert("Can't index table because: " + error);
            }
        });
    };

    // Button to add default cell
    let defaultCellButton = () => {
        Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'Add default cell',
                'icon': 'fa-play-circle',
                'handler': add_cell
            }, 'add-default-cell', 'Default cell')
        ])
    };

    // Run on start
    let load_ipython_extension = () => {
        // Add a default cell if there are no cells
        if (Jupyter.notebook.get_cells().length === 1) {
            add_cell();
        }
        defaultCellButton();
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});