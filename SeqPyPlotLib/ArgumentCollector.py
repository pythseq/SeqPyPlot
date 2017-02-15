import argparse
import sys
import os


class Args:
    def __init__(self):
        self.args = self.arg_parser()
        self.args.time = self.time_parser()
        self.args.condition = self.condition_label_parser()

        if not os.path.isdir(self.args.out):
            os.makedirs(self.args.out)

        self.path = os.path.join(self.args.out, self.args.prefix)

    def arg_parser(self):
        # type: () -> NameSpace()
        parser = argparse.ArgumentParser(description='Required: -raw_data or -plot_data',
                                         prog='SeqPyPlot v0.2')

        # plotter args
        parser.add_argument('-time',
                            metavar='d1,d2,d3',
                            default=None,
                            type=str,
                            dest='time',
                            help='A comma separated list of time points.')

        parser.add_argument('-out',
                            metavar='Default_out',
                            default='Default_out',
                            type=str,
                            dest='out',
                            help='Output Folder Name')

        parser.add_argument('-prefix',
                            type=str,
                            default='SeqPyPlot_default',
                            metavar='SeqPyPlot_',
                            dest='prefix',
                            help='Leading name of output file.')

        parser.add_argument('-data_type',
                            metavar='htseq',
                            default='htseq',
                            type=str,
                            dest='datatype',
                            help='Either cuffnorm, cuffdiff, deseq2, or edgeR.')

        parser.add_argument('-c',
                            metavar='S1,S2',
                            default=('Series1,Series2'),
                            type=str,
                            dest='condition',
                            help='\tA comma separated list of conditions (max 2)')

        ## Filter args
        parser.add_argument('-low',
                            metavar='0',
                            default=25,
                            type=float,
                            dest='low',
                            help='Default: 2. Set the min expression value to accept.')
        parser.add_argument('-hi',
                            metavar='5000000',
                            default=5000000,
                            type=float,
                            dest='hi',
                            help='Default: 5mil. Set the max expression value to accept.')
        parser.add_argument('-dif',
                            metavar='60',
                            default=60,
                            type=float,
                            dest='dif',
                            help='Default: 60. Set minimum difference in expression.')
        parser.add_argument('-log2',
                            metavar='1.0',
                            default=1.0,
                            type=float,
                            dest='log',
                            help='Default: 1.0. Minimum log2 change to accept.')

        parser.add_argument('-num',
                            metavar='2',
                            default=2,
                            type=int,
                            dest='num',
                            help='Default: 2. Set number of plots.')

        parser.add_argument('-r',
                            default=False,
                            action='store_true',
                            dest='remove',
                            help='Default: False. Use to remove genes not always on.')

        parser.add_argument('-tally',
                            action='store_true',
                            default=False,
                            dest='tally',
                            help='Default: False. Tally DE genes.')

        parser.add_argument('-report',
                            action='store_true',
                            default=False,
                            dest='report',
                            help='Default: False. Write plot data and filter results.')

        parser.add_argument('-ercc',
                            action='store_true',
                            default=False,
                            dest='ercc',
                            help='Default: False. Write ERCC data to an output file.')

        parser.add_argument('-raw_data',
                            type=str,
                            default=None,
                            metavar='None',
                            dest='raw_data',
                            help='Input file or folder.')

        parser.add_argument('-plot_data',
                            type=str,
                            default=None,
                            metavar='None',
                            dest='plot_data',
                            help='Formatted input data to plot')

        parser.add_argument('-gene_list',
                            type=str,
                            default=None,
                            metavar='None',
                            dest='gene_list',
                            help='\tSingle Column Gene list in txt file.')

        parser.add_argument('-input_results',
                            type=str,
                            default=None,
                            metavar='None',
                            dest='de_results',
                            help='Optional. Your own flagged gene list.')

        return parser.parse_args()

    @staticmethod
    def __label_parser(argument):
        # type: (character_string) -> list of strings
        try:
            parsed_list = [x for x in argument.split(',')]
            return parsed_list

        except AttributeError:
            print("The group labels have to be comma separated.")
            sys.exit()

    def time_parser(self):
        return self.__label_parser(str(self.args.time))

    def condition_label_parser(self):
        return self.__label_parser(str(self.args.condition))

    def make_logs(self):

        with open((str(self.path) + ".log.txt"), "w+") as logfile:

            logfile.write(
                "\nLogs for {0}:".format(str(self.args.out)))

            logfile.write(
                "\nExpression thresholds is: \n-Upper expression limit: {}\n-Lower expression limit: {}\n-Minimum Difference: {}\n".format(
                    self.args.hi, self.args.low, self.args.dif))

            logfile.write(
                "\nLog2Fold threshold is: " + str(self.args.log) + "\n")

args = Args()