import PySimpleGUI as sg
import configparser
import subprocess
import os

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

def main():

    sg.theme('Topanga')

    main_panel = [
        [sg.Text('Input Folder', size=(15, 1)), sg.Input(key='inputMainPanelMeshFolder'), sg.FolderBrowse(target=('inputMainPanelMeshFolder'))],

        # Input and output
        [sg.Text('# Output options.', size=(55, 2))],

        [sg.Text('Output Path', size=(15, 1)), sg.Input(default_text="/", key='output_path'), sg.FolderBrowse(target=('output_path'))],

        [sg.Text('High Poly name suffix', size=(55, 1)),
         sg.Input(default_text = "_high", size=(20,15), key="name_suffix_high")], # STRING

        [sg.Text('Low Poly name suffix.', size=(55, 1)),
         sg.Input(default_text = "_low", size=(20,15), key="name_suffix_low")], # STRING

        [sg.Text('Output format', size=(55, 1)),
         sg.Combo(['surface', 'dds', 'bmp', 'jpg', 'jif', 'jpeg', 'jpe', 'png', 'tga', 'targa', 'tif', 'tiff', 'wap', 'wbmp', 'wbm', 'psd', 'psb', 'hdr', 'exr', 'webp'], default_value='png', size=(15, 1), key="output_format")],

         # ambient-occlusion options
        [sg.Text('                  ', size=(55, 2))],
        [sg.Text('# Ambient occlusion options.', size=(55, 2))],

        [sg.Text('Antialiasing method.', size=(55, 1)),
         sg.Combo(['None', 'Subsampling 2x2', 'Subsampling 4x4', 'Subsampling 8x8'], default_value='None', size=(15, 1), key="antialiasing")],

        [sg.Text('Resolution', size=(55, 1)),
         sg.Combo(['512', '1024', '2048', '4096'], default_value='1024', size=(15, 1), key="resolution")],

        [sg.Text('Enable Floor', size=(55, 1)),
         sg.Checkbox('Enable Floor', default=True, size=(15, 1), key="enable_ground_plane")],

        [sg.Text('Floor Offset.', size=(55, 1)),
         sg.Input(default_text = "0", size=(20,15), key="ground_offset")], # STRING

        # Buttons
        [sg.Text('                  ', size=(55, 2))],
        [sg.Button('Start processing folder', size=(25, 1), key='utility_RunSbsbaker')],

    ]

    layout = [
                [sg.TabGroup(
                    [
                        [
                        sg.Tab('Sbsbaker Utility', main_panel, tooltip='Sbsbaker Utility'),
                        ]
                    ])
                ],
                [sg.Cancel(key='quit')],
            ]

    window = sg.Window('Sbsbaker Utility', layout)


    while (True):

        # This is the code that reads and updates your window
        event, values = window.Read(timeout=100)

        if event == 'Exit' or event is None:
            break

        if event == 'quit':
            break

        # Vpype Flow Imager
        if event == 'utility_RunSbsbaker':
            if values['inputMainPanelMeshFolder']:

                for root, dirs, files in os.walk(values['inputMainPanelMeshFolder']):
                    for filename in files:
                        if filename.lower().endswith(('.fbx')):

                            file_path = os.path.join(root, filename)

                            # Generate parameters
                            args = str(config['locations']['sub_auto_tool'])
                            args += str("sbsbaker.exe ambient-occlusion-from-mesh") # File
                            args += ' --inputs "' + str(file_path) +'"' # Mesh files to process. This option is implicit, so you can just provide a list of files at the end of your arguments, they will be interpreted as inputs.
                            args += ' --name-suffix-high ' + str(values['name_suffix_high']) # High Poly name suffix.
                            args += ' --name-suffix-low ' + str(values['name_suffix_low']) # Low Poly name suffix.
                            args += ' --output-format ' + str(values['output_format']) # Format to use for output image file.

                            output_path = values['output_path'];
                            if (output_path == '/'):
                                output_path = os.path.join(file_path, '..')
                            args += ' --output-path "' + str(output_path) + '"'# Set the output path for the generated files. By default the output path is the current directory.

                            antialiasings = {
                                'None': 0,
                                'Subsampling 2x2': 1,
                                'Subsampling 4x4': 2,
                                'Subsampling 8x8': 3,
                            }
                            antialiasing = antialiasings.get(values['antialiasing'], 0)
                            # args += ' --antialiasing ' + str(antialiasing) # Antialiasing method.

                            # --apply-diffusion # Whether to use diffusion as a post-process after dilation, or not.
                            # --attenuation # How occlusion is attenuated by occluder distance (0='None', 1='Smooth', 2='Linear')
                            # --average-normals # Compute rays directions based on averaged normals.

                            args += ' --enable-ground-plane ' + str(values['enable_ground_plane']).lower() # If enabled, adds an infinite plane under the baked mesh.
                            args += ' --ground-offset ' + str(values['ground_offset']) # Offset of the ground plane from the mesh lowest point.

                            resolutions = {
                                "512": 9,
                                "1024": 10,
                                "2048": 11,
                                "4096": 12,
                            }
                            resolution = resolutions.get(values['resolution'], 11)
                            args += ' --output-size ' + str(resolution) + ',' + str(resolution) # Output size of the generated map.<w> and <h> are the exponents of powers of 2 that give the actual width and height.

                            # --self-occlusion

                            args += ' --use-lowdef-as-highdef true' # Skip scene request

                            # print(args)
                            subprocess.Popen(args)
            else:
                sg.popup_error('Please select a valid folder')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
