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
        [sg.Text('Input Folder', size=(15, 1)), sg.Input(key='inputMainPanelMeshFolder'), sg.FolderBrowse(target=(-1, 0))],

        [sg.Text('Flow field PRNG seed (overriding the main --seed)', size=(55, 1)),
         sg.Slider(range=(0,100), default_value=25, size=(20,15), orientation='horizontal', key="vfi_flow_seed")], # INTEGER

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
                outputFile = values['inputMainPanelMeshFolder'][:-3] + '-.svg'

                # Generate parameters
                args = ''
                args =+ 'noise_coeff= ' + str(values['vfi_noise_coeff'])
                args =+ 'n_fields= ' + str(values['vfi_n_fields'])
                args =+ 'min_sep= ' + str(values['vfi_min_sep'])
                args =+ 'max_sep= ' + str(values['vfi_max_sep'])
                args =+ 'max_length= ' + str(values['vfi_max_length'])
                args =+ 'max_size= ' + str(values['vfi_max_size'])
                args =+ 'seed= ' + str(values['vfi_seed'])
                args =+ 'flow_seed= ' + str(values['vfi_flow_seed'])
                print(args)
                # subprocess.Popen('vpype flow_img "' + str(values['inputMainPanelMeshFolder']) + '" write "' + str(outputFile) + '"')
            else:
                sg.popup_error('Please select a valid .jpg file')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
