import time
import os
import sys
import SeqPyPlotLib.DataContainer as DataContainer

from SeqPyPlotLib.DataPlotter import MainDataPlotter
from SeqPyPlotLib.DataAnalyzer import DataAnalyzer
from SeqPyPlotLib.ArgumentCollector import Args

if __name__ == '__main__':

    start = float(time.time())
    print '\n\n'
    # Collect args
    argz = Args()
    argz.make_logs()
    args = argz.args


    # if files aren't provided properly
    if args.raw_data == args.plot_data is None:
        print("\nProvide either a (raw_data file) or (plot_data file)\n")
        os.system('python SeqPyPlot.py -h')
        sys.exit()

    elif args.raw_data is not None and args.plot_data is not None:
        print ("ERROR...")
        print "\nLoad either raw_data or pre-formatted plot_data. Don't load both!\n"
        sys.exit()
    elif args.raw_data is not None and args.gene_list is not None:
        print("ERROR...")
        print "\nRun the program on raw_data, then rerun supplying the _plotter_data.txt file.\n"
        sys.exit()
    else:
        pass

    # if only raw data is supplied

    if args.raw_data is not None:
        FullContainer = DataContainer.DataContainer(args)  # object containing parsed raw_data
        Analyzer = DataAnalyzer(args, FullContainer)  # object used for filtering data and writing out filtered data files

        Analyzer.seqpyfilter()  # object containing analyzed data

        DataPrinter = DataContainer.DataPrinter(args, FullContainer, Analyzer)
        DataPrinter.write_plot_data()
        DataPrinter.write_de_results()
        DataPrinter.write_filtered_data()

        if args.ercc:
            DataPrinter.write_ercc_data()

        if args.tally:
            Plot_Builder = MainDataPlotter(args, Analyzer, None)  # object used for generating plots
            Plot_Builder.de_bar('black')
            Plot_Builder.plot_tally()
            Plot_Builder.plot_histograms()
            Analyzer.print_analyzer_results()

        print(
            "Data analyzed, select genes for plotting from {}_filtered.txt and rerun the program with plot data.".format(
                args.out))
        # args.make_logs()
        sys.exit()

    elif args.plot_data is not None:
        if args.gene_list is not None:  # if plot data and gene list is provided

            # Create Output files
            DataContainer.PrepareOutputDirectory.make_folder(args.out)

            FullContainer = DataContainer.DataContainer(args)  # object containing parsed premade plot data
            if args.de_results is not None:  # if no results are provided, calculate them and then load them
                FullContainer.load_results()
                Analyzer = DataAnalyzer(args, FullContainer)
            else:
                Analyzer = DataAnalyzer(args, FullContainer)

            Analyzer.seqpyfilter()

            assert FullContainer.analyzed

            # Ready, get set....
            FigureList = DataContainer.MakeFigureList(args)  # object containing gene list for plotting and other attributes
            Plot_Builder = MainDataPlotter(args, Analyzer, FigureList)  # object used for generating plots

            if args.report:
                DataPrinter = DataContainer.DataPrinter(args, FullContainer, Analyzer)
                DataPrinter.write_plot_data()
                DataPrinter.write_de_results()
                DataPrinter.write_filtered_data()

            if args.tally:
                Plot_Builder.de_bar('black')
                Plot_Builder.plot_tally()
                Plot_Builder.plot_histograms()
                Analyzer.print_analyzer_results()

            Plot_Builder.plot_figures()
        else:
            # perform the DE analysis using processed plot data
            FullContainer = DataContainer.DataContainer(args)
            Analyzer = DataAnalyzer(args, FullContainer)
            Analyzer.seqpyfilter()
            Plot_Builder = MainDataPlotter(args, Analyzer, None)

            DataPrinter = DataContainer.DataPrinter(args, FullContainer, Analyzer)
            DataPrinter.write_de_results()
            DataPrinter.write_filtered_data()

            # if args.tally:
            Plot_Builder.de_bar('black')
            Plot_Builder.plot_histograms()
            Analyzer.print_analyzer_results()

            print "Finished."
            sys.exit()
    else:
        os.system('python SeqPyPlot.py -h')
        sys.exit()

    end = float(time.time())
    print("Total Run Time: {}".format((end - start) / 60.0))
    # args.make_logs()

