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
    const cfg = {
        'window_display': false,
        'cols': {
            'lenName': 24,
            'lenType': 16,
            'lenVar': 40
        },
        'kernels_config' : {
            'python': {
                library: 'var_list.py',
                delete_cmd_prefix: 'del ',
                delete_cmd_postfix: '',
                varRefreshCmd: 'print(var_dic_list())'
            }
        },
        'types_to_exclude': ['module', 'function', 'builtin_function_or_method', 'instance', '_Feature']
    };

    const getCookie = (name) => {
        const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    };

    const indexTable = varName => {
        const kernel_id = String(Jupyter.notebook.kernel.id);

        const send_url = utils.url_path_join(Jupyter.notebook.base_url, '/juneau-2');

        const data_json = {
            'var': varName,
            '_xsrf': getCookie("_xsrf"),
            'kernel_id': kernel_id
        };

        $.ajax({
            url: send_url,
            method: 'PUT',
            data: data_json,
            dataType: 'json',
            timeout: 10000000,
            success: function (response) {
                console.log(`----${varName} is successfully indexed!----`);
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

    // Add a cell above current cell (will be top if no cells)
    const add_cell = () => {
        // Define default cell here
        indexTable('df');

        $([0, 1, 2, 3, 4]).each(function () {
            const i = this;
            indexTable(`df${i}`)
        });

        // for (let i = 1; i < 6; i++) {
        //     indexTable(`df${i}`)
        // }
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
        console.log(String(Jupyter.notebook.kernel.id));
        defaultCellButton();
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});