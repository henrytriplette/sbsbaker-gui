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
        [sg.Text('Output options.', size=(55, 1))],

        [sg.Text('Output Path', size=(15, 1)), sg.Input(default_text="/", key='output_path'), sg.FolderBrowse(target=('output_path'))],

        [sg.Text('High Poly name suffix', size=(55, 1)),
         sg.Input(default_text = "_high", size=(20,15), key="name_suffix_high")], # STRING

        [sg.Text('Low Poly name suffix.', size=(55, 1)),
         sg.Input(default_text = "_low", size=(20,15), key="name_suffix_low")], # STRING

        [sg.Text('Output format', size=(55, 1)),
         sg.Combo(['surface', 'dds', 'bmp', 'jpg', 'jif', 'jpeg', 'jpe', 'png', 'tga', 'targa', 'tif', 'tiff', 'wap', 'wbmp', 'wbm', 'psd', 'psb', 'hdr', 'exr', 'webp'], default_value='png', size=(15, 1), key="output_format")],

         # ambient-occlusion options
        [sg.Text('Ambient occlusion options.', size=(55, 1))],



        [sg.Text('Resolution', size=(55, 1)),
         sg.Combo(['512', '1024', '2048', '4096'], default_value='1024', size=(15, 1), key="resolution")],

        # Buttons
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
                            print(filename)

                            # Generate parameters
                            args = config['locations']['sub_auto_tool']
                            args =+ '\sbsbaker.exe ambient-occlusion' # File
                            args =+ ' --inputs ' + str(filename) # Mesh files to process. This option is implicit, so you can just provide a list of files at the end of your arguments, they will be interpreted as inputs.
                            args =+ ' --name-suffix-high ' + str(values['name_suffix_high']) # High Poly name suffix.
                            args =+ ' --name-suffix-low ' + str(values['name_suffix_low']) # Low Poly name suffix.
                            args =+ ' --output-format ' + str(values['output_format']) # Format to use for output image file.
                            args =+ ' --output-path ' + str(values['output_path']) # Set the output path for the generated files. By default the output path is the current directory.

                            print(args)
                            # subprocess.Popen(args)
            else:
                sg.popup_error('Please select a valid folder')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
