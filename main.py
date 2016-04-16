# This is the file that starts the GUI.
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/minimal-app.html

# Icons used:
# https://design.google.com/icons/#ic_mic
# https://design.google.com/icons/#ic_close
# https://design.google.com/icons/#ic_playlist_play


import tkinter as tk
import tkinter.font as tk_font
from tkinter import messagebox as mbox
import listener
import wave
import numpy as np
import specto
import asr
import os

# Reference for icon usage:
# http://stackoverflow.com/q/4297949

# Reference for font usage:
# http://stackoverflow.com/a/20588878
ASR_SERVICE = "Google Speech API"
class SpectoApp(tk.Frame):
    def __init__(self, master=None):

        tk.Frame.__init__(self, master)

        self.grid()
        self.images = {
            'record': tk.PhotoImage(file="Icons/ic_mic_black_36dp_1x.png"),
            'create': tk.PhotoImage(file="Icons/ic_playlist_play_black_36dp_1x.png"),
            'close': tk.PhotoImage(file="Icons/ic_close_black_36dp_1x.png")
        }  # We need to keep a reference to the image objects.
        self.font = tk_font.Font(family="Helvetica", size=18, weight='bold')
        self.check_font = tk_font.Font(family="Times", size=12)
        self.listener_input_dict = {
            'record_seconds': {
                'label': 'Recording length',
                'type': int,
                'desc': 'Recording time in seconds.',
                'default': 5
            },
            'rate': {
                'label': 'Recording rate',
                'type': int,
                'desc': 'Rate in bits/sec',
                'default': 44100
            }
        }
        self.text = "no ASR"
        self.listener_input_list = list(self.listener_input_dict.keys())
        self.listener_input_list.sort()

        dropdown_var = tk.StringVar(master=self)
        dropdown_var.set("Sequential(2) gist_heat")
        self.specto_input_dict = {
            'NFFT': {
                'label': 'NFFT',
                'type': int,
                'desc': 'NFFT Window Size. (Ideally power of 2)',
                'default': 256
                },
            'noverlap': {
                'label': 'Window Overlap',
                'type': int,
                'desc': 'Overlap Size has to be less than NTFT',
                'default': 128
                },
            'minfreq': {
                'label': 'Min Freq',
                'type': int,
                'desc': 'Minimum Frequency for the Y-Axis',
                'default': 100
                },
            'maxfreq': {
                'label': 'Max Freq',
                'type': int,
                'desc': 'Maximum Frequency for the Y-Axis',
                'default': 4000
                },
            'cmap': {
                'label': 'Color Map',
                'type': specto.get_cm_color_enum,
                'desc': 'See http://matplotlib.org/examples/color/colormaps_reference.html',
                'is_dropdown': True,
                'default': 'gist_heat',
                'variable': dropdown_var,
                'options': specto.get_color_maps()  # This is a generator, but could be a list or any sequence.
            }
        }
        self.specto_input_list = list(self.specto_input_dict.keys())
        self.specto_input_list.sort()

        # This is silly, but I want dropdowns to be at the bottom. They can ignore tha alphabetical order!
        for option in self.specto_input_dict:
            if self.specto_input_dict[option].get('is_dropdown', False) is True:
                self.specto_input_list.remove(option)
                self.specto_input_list.append(option)

        self.listener_input_rows = {}
        self.specto_input_rows = {}

        row_num = self.input_rows_generator(0, self.listener_input_dict, self.listener_input_list, self.listener_input_rows)
        row_num = self.input_rows_generator(row_num, self.specto_input_dict, self.specto_input_list, self.specto_input_rows)

        self.freq_grid_bool = tk.IntVar()
        row_num += 1
        freq_grid_button = tk.Checkbutton(master=self, text="Create freq grid", variable=self.freq_grid_bool, anchor=tk.W,
                                    font=self.check_font)
        freq_grid_button.grid(row=row_num, column=1, in_=self)


        self.time_grid_bool = tk.IntVar()
        row_num += 1
        time_grid_button = tk.Checkbutton(master=self, text="Create time grid", variable=self.time_grid_bool, anchor=tk.W,
                                          font=self.check_font)
        time_grid_button.grid(row=row_num, column=1, in_=self)

        self.asr_bool = tk.IntVar()
        row_num += 1
        asr_button = tk.Checkbutton(master=self, text="Use ASR", variable=self.asr_bool, anchor=tk.W,
                                    font=self.check_font)
        asr_button.grid(row=row_num, column=1, in_=self)

        self.create_widgets(row_num+1)

    def create_widgets(self, row_num):
        self.rec_button = tk.Button(self, text="Record", command=self.record,
                                    image=self.images['record'], compound=tk.RIGHT, font=self.font)
        self.rec_button.grid(row=row_num, column=0, padx=10, pady=10)

        self.gen_button = tk.Button(self, text="Generate", command=self.generate,
                                    image=self.images['create'], compound=tk.RIGHT, font=self.font)
        self.gen_button.grid(row=row_num, column=1, padx=10, pady=10)

        self.quit_button = tk.Button(self, text="Close", command=self.quit,
                                     image=self.images['close'], compound=tk.RIGHT, font=self.font)
        self.quit_button.grid(row=row_num, column=2, padx=10, pady=10)

    # Reference tutorial: http://www.tutorialspoint.com/python/tk_entry.htm
    # A helper function that creates an input row for the table form.
    # input_dict contains all of the relevant info on the fields that
    # we will generate. input_list just contains the same keys but sorted in order.
    def input_rows_generator(self, row_num, input_description_dict, input_list, input_rows):
        for var_name in input_list:
            current_row = []
            label = tk.Label(text=input_description_dict[var_name]['label'])
            label.grid(row=row_num, column=0, sticky=tk.W, in_=self)
            current_row.append(label)

            input_field = None
            if input_description_dict[var_name].get('is_dropdown', False) is False:
                input_field = tk.Entry()
                # Ref: http://stackoverflow.com/a/20126024
                input_field.insert(tk.END, input_description_dict[var_name]['default'])
            else:
                input_field = self.create_dropdown(input_description_dict[var_name])

            input_field.grid(row=row_num, column=1, in_=self)
            current_row.append(input_field)

            desc = tk.Label(text=input_description_dict[var_name]['desc'])
            desc.grid(row=row_num, column=2, padx=2, pady=2, in_=self)
            current_row.append(desc)

            input_rows[var_name] = current_row
            row_num += 1

        return row_num

    def create_dropdown(self, dropdown_info):
        # Reference: http://effbot.org/tkinterbook/optionmenu.htm
        option = tk.OptionMenu(self, dropdown_info['variable'], *dropdown_info['options'])
        return option

    # Helper function that just returns a dictionary
    # mapping each argument to its casted value.
    def get_value_dict(self, rows_dict, info_dict):
        return_dict = {}
        for arg in rows_dict:
            # This is defined in the original input dict. Something like int or str or float...
            type_func = info_dict[arg]['type']
            # the input_rows dict looks like this:
            # 'NTFT':[labelObj, EntryField, DescLabel]
            if info_dict[arg].get('is_dropdown', False) is False:
                return_dict[arg] = type_func(rows_dict[arg][1].get())
            else:
                return_dict[arg] = type_func(info_dict[arg]['variable'].get())
        return return_dict

    def record(self):
        listener_args = self.get_value_dict(rows_dict=self.listener_input_rows, info_dict=self.listener_input_dict)
        listener.record_file(**listener_args)
        #

    def generate(self):
        if not os.path.exists(listener.WAVE_OUTPUT_PATH):
            mbox.showwarning(
                "File not found.",
                "No file found in %s. Please record audio before pressing generate." % listener.WAVE_OUTPUT_PATH
            )
            return
        spectogram_args = self.get_value_dict(rows_dict=self.specto_input_rows, info_dict=self.specto_input_dict)
        spec = specto.Specto()
        with wave.open(listener.WAVE_OUTPUT_PATH, 'rb') as spf:
            signal = spf.readframes(-1)
            signal = np.fromstring(signal, 'Int16')
            Fs = spf.getframerate()
            spectogram_args['Fs'] = Fs
            plt = spec.create_specto(signal, spectogram_args)
            size = (int)(len(signal)/2)
            #spec.create_freq(signal[size:], Fs)
            if self.freq_grid_bool.get():
                spec.create_freq_grid(signal, Fs, maxfreq=spectogram_args['maxfreq'])
            if self.time_grid_bool.get():
                spec.create_time_grid(signal, Fs)

        plt.show()

        if self.asr_bool.get():
            spec.add_text("Waiting for ASR service (%s)" % ASR_SERVICE)
            self.text = asr.recognize_file(listener.WAVE_OUTPUT_PATH)
            print(self.text)

            # Sample return:
            # self.text = {'alternative': [{'confidence': 0.98104376, 'transcript': 'this is a test how are you'}, {'transcript': 'this is a test how are U'}, {'transcript': 'this is a test how are youuu'}, {'transcript': 'this is a test how R you'}], 'final': True}

            if not self.text:
                spec.add_text("ASR Service (%s) did not return results." % ASR_SERVICE)
            else:
                spec.add_text(compose_ASR_string(self.text))


# Assumes we are working with the Google Speech API
def compose_ASR_string(raw_input):
    ret_list = []
    if not raw_input['final']:
        ret_list.append("Could not verify voice input.")
        return '\n'.join(ret_list)
    ret_list.append("ASR results (most to least likely):")
    for transcript in raw_input['alternative']:
        if 'confidence' in transcript:
            ret_list.append('%s  |  Confidence: %f' % (transcript['transcript'], transcript['confidence']) )
        else:
            ret_list.append('%s' % transcript['transcript'])

    return '\n'.join(ret_list)


if __name__ == "__main__":
    app = SpectoApp()
    app.master.title("Speech to Spectogram")
    app.mainloop()