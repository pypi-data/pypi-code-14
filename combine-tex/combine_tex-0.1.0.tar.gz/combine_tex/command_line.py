import argparse
import re
import os
import shutil


class CombineTexParser(object):
    def __init__(self, infile, outfolder):
        self.num_figures_processed = 0
        self.outfolder = outfolder
        self.infile = infile

    @staticmethod
    def parse_line(line):
        m = re.search('input\{([^\}]*)', line)
        if m:
            return m.group(1)
        else:
            return None

    @staticmethod
    def parse_for_figure(line):
        m = re.search('\{(\S*\/([^\/]*\.pdf))\}', line)
        if m:
            return m.group(1), m.group(2)
        else:
            return None, None

    def remake_figure_line(self, line):
        self.num_figures_processed += 1
        fig_name = 'f'
        if self.num_figures_processed < 10:
            fig_name += '0' + str(self.num_figures_processed)
        else:
            fig_name += str(self.num_figures_processed)
        fig_name += '.pdf'
        return re.sub(r'\{(\S*\/([^\/]*\.pdf))\}', '{' + fig_name + '}', line), fig_name

    def find_file_depends(self, filename):
        infile = open(filename)
        file_list = []
        for line in infile:
            depending_file = self.parse_line(line)
            if depending_file:
                file_list.append(depending_file)
                more_files = self.find_file_depends(depending_file)
                if more_files:
                    file_list.append(more_files)
        return file_list

    def add_file_to_stream(self, file_name, out_stream):
        infile = open(file_name)
        for line in infile:
            depending_file = self.parse_line(line)
            if depending_file:
                self.add_file_to_stream(depending_file, out_stream)
            else:
                figure_path, fig_name = self.parse_for_figure(line)
                if figure_path:
                    line, fig_name = self.remake_figure_line(line)
                    shutil.copy2(figure_path, os.path.join(self.outfolder, fig_name))
                out_stream.write(line)

    def convert_to_one_file(self):
        outfile = open(self.outfolder + '/' + self.infile, 'w+')
        self.add_file_to_stream(self.infile, outfile)

    def make_folders(self):
        if not os.path.exists(self.outfolder):
            os.makedirs(self.outfolder)
            # os.makedirs( outFolder + '/' + 'figures' )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    inputfilename = args.input
    outputfoldername = args.output

    parser = CombineTexParser(inputfilename, outputfoldername)
    parser.make_folders()
    parser.convert_to_one_file()
    shutil.copy2('references.bib', outputfoldername + '/')
