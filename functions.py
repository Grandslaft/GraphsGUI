from src.functions.physics_graphs import (
    FeCr_phase_graph, FeCrAl_phase_graph, 
    FeCr_phase_model, FeCrAl_phase_model
)

'''
Explained Parameters of the Functions Dictionary Needed for Adding New Graphs to the GUI

button_name: The label displayed on the button and used as the Graph Widget's title.

params_explanation: A brief explanation of the required parameters for the function.

graph_sublots: Defines the layout of subplots (rows and columns).

graph_titles: A list of titles for individual graphs, either static or dynamically generated.

graph_types: Specifies the type of graph (e.g., lines, heatmap).

required_params: A dictionary of required parameters with default values.

axis_titles: Titles for the x and y axes of the graphs.

scale: Defines the scale for both x and y axes (e.g., linear, log).

lim: Specifies axis limits; None if no specific limit is required.

function: The function that generates the graph.

name_start: The prefix for saving heatmap plot data.

prec_col_name: The prefix for saving precipitate-related data.

folder_name: Defines the folder name for saving files, static or dynamically generated.

default_file_name: The default file name for saving output, static or dynamically generated.
'''

functions = [
    dict(
        button_name = "Фазова діаграма для сплаву Fe-Cr-Al у рівноважних умовах",
        params_explanation = "Введіть параметр xAl (від 0 до 0.2)",
        graph_sublots=dict(
            nrows=1,
            ncols=1
        ),
        graph_titles = [
            "Фазова діаграма для сплаву Fe-Cr-Al у рівноважних умовах"
        ],
        graph_types = [
            'lines'
        ],
        required_params = dict(
            xAl = 0,
        ),
        axis_titles = [
            [None, None],
        ],
        scale = [
            ['linear', 'linear'],
        ],
        lim = [
            [None, None],
        ],
        function = FeCr_phase_graph,
        dat_data = (),
        dat_cols = ('x\ty\t',),
        folder_name = '',
        default_file_name = lambda xAl: f"T(xCr)_Al{xAl:.0f}",
    ),
    dict(
        button_name = "Фазова діаграма для опроміненого сплаву Fe-Cr-Al",
        params_explanation = "Введіть параметри xCr, xAl (від 0 до 0.2), N (Натуральне число), r0 (Натуральне число)",
        graph_sublots=dict(
            nrows=1,
            ncols=1
        ),
        graph_titles = [
             "Фазова діаграма для опроміненого сплаву Fe-Cr-Al"
        ],
        graph_types = [
            'lines'
        ],
        required_params = dict(
            xCr = 30,
            xAl = 5,
            N = 30,
            r0 = 4,
        ),
        axis_titles = [
            [None, None],
        ],
        scale = [
            ['linear', 'linear'],
        ],
        lim = [
            [None, None],
        ],
        function = FeCrAl_phase_graph,
        dat_data = (),
        dat_cols = ('x\ty\t', 'x\ty\t'),
        folder_name = '',
        default_file_name = lambda xCr, xAl, N, r0: f"K(T)_Cr{xCr:.0f}%Al{xAl:.0f}%_N{N:.0f}_r0{r0}",
    ),
    dict(
        button_name = "Моделювання відпалу твердого розчину",
        params_explanation = "Введіть параметр xAl (від 0 до 0.2)",
        graph_sublots=dict(
            nrows=2,
            ncols=2
        ),
        graph_titles = [
            'Просторовий розподіл Хрому', 
            'Просторовий розподіл Алюмінію', 
            'Еволюція середнього розміру преципітатів Хрому', 
            'Еволюція густини преципітатів Хрому'
        ],
        graph_types = [
            'heatmap',
            'heatmap',
            'lines',
            'lines'
        ],
        required_params = dict(
            Cr0 = 30,
            Al0 = 5,
            T = 710,
            max_t = 1000,
            write_every_t = 200,
            Size = 64,
        ),
        axis_titles = [
            [None, None],
            [None, None],
            ['Time [hours]', '<Rp> [nm]'],
            ['Time [hours]', 'N x 10^(-27) [m^-3]']
        ],
        scale = [
            ['linear', 'linear'],
            ['linear', 'linear'],
            ['linear', 'linear'],
            ['linear', 'linear'],
        ],
        lim = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
        ],
        function = FeCr_phase_model,
        name_start = [
            'Cr(r)',
            'Al(r)'
        ],
        dat_data = (2, 3),
        dat_cols = ('Time [hours]\t<Rp> [nm]\t', 'Time [hours]\tNp x 1E-27 [m^3]\t'),
        folder_name = lambda Size, Cr0, Al0, T: f"M{Size:.0f}_Cr{Cr0:.0f}%Al{Al0:.0f}%_T{T:.0f}",
        default_file_name = lambda name_start, Size, time, Cr0, Al0, T: f"{name_start}{Size:.0f}_t{time:.0f}_Cr{Cr0:.0f}%Al{Al0:.0f}%_T{T:.0f}",
    ),
    dict(
        button_name = "Моделювання опромінення",
        params_explanation = "Введіть параметри xCr, xAl (від 0 до 0.2), N (Натуральне число), r0 (Натуральне число)",
        graph_sublots=dict(
            nrows=2,
            ncols=2
        ),
        graph_titles = [
            'Просторовий розподіл Хрому', 
            'Просторовий розподіл Алюмінію', 
            'Еволюція середнього розміру преципітатів Хрому', 
            'Еволюція густини преципітатів Хрому'
        ],
        graph_types = [
            'heatmap',
            'heatmap',
            'lines',
            'lines'
        ],
        required_params = dict(
            Cr0 = 30,
            Al0 = 5,
            T = 710,
            K = 1E-6,
            N = 30,
            r0 = 1,
            max_dose = 6,
            write_every_dose = 1,
            Size = 64,
        ),
        axis_titles = [
            [None, None],
            [None, None],
            ['Dose [dpa]', '<Rp> [nm]'],
            ['Dose [dpa]', 'N x 10^(-27) [m^-3]']
        ],
        scale = [
            ['linear', 'linear'],
            ['linear', 'linear'],
            ['linear', 'linear'],
            ['linear', 'linear'],
        ],
        lim = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
        ],
        function = FeCrAl_phase_model,
        name_start = [
            'Cr(r)',
            'Al(r)'
        ],
        dat_data = (2, 3),
        dat_cols = ('Dose [dpa]\t<Rp> [nm]\t', 'Dose [dpa]\tNp x 1E-27 [m^3]\t'),
        folder_name = lambda Size, Cr0, Al0, T, K, N, r0: f"M{Size:.0f}_Cr{Cr0:.0f}%Al{Al0:.0f}%_T{T:.0f}_K{K*1e6:.0f}E-6_N{N:.0f}_r0{r0}",
        default_file_name = lambda name_start, Size, time, Cr0, Al0, T, K, N, r0: f"{name_start}{Size:.0f}_t{time:.0f}_Cr{Cr0:.0f}%Al{Al0:.0f}%_T{T:.0f}_K{K*1e6:.0f}E-6_N{N:.0f}_r0{r0:.0f}",
    ),
]