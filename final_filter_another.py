import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import trackpy as tp

# constants change to your parameters
MPP = 0.116
FPS = 20

def plot_msd(track_data:pd.DataFrame, title='Remember what graphs to filter'):
       '''
       plot msd graphs in log scale with labels
       '''
       # Calculate time msd
       time_msd = tp.imsd(track_data, mpp=MPP, fps=FPS)

       fig, (ax1, ax2) = plt.subplots(1,2,
                     figsize=(15,5),
                     gridspec_kw={
                            'width_ratios': [2,1],
                            'height_ratios': [1]})
       # graph trajectories
       ax1 = tp.plot_traj(track_data, ax=ax1, label=True)
       ax1.set_title('Particle trajectories')

       # graph msd by particle
       ax2.plot(time_msd.index, time_msd)
       ax2.set_ylabel(r'avg($\Delta r^2 $) [$\mu$m$^2$]')
       ax2.set_xlabel('lag time $t$ (sec)')
       ax2.set_xscale('log')
       ax2.set_yscale('log')
       ax2.set_title('Time MSD by particle')
       # legend to the right of ax1 (outside the plot)
       ax2.legend(time_msd.keys(), bbox_to_anchor=(1.04,0.5), loc="center left")
         
       fig.suptitle(title)
       fig.tight_layout()
       fig.show()


def main():
       # loads the output excel file of the traking algorithms
       file_path = input("insert final_track.xlsx path ")
       track_data = pd.read_excel(file_path)


       # remove unwanted particles #
       #############################
       while True: # loop until wer'e fine with the result
              # show time msd graphs
              plot_msd(track_data)

              # ask what graphs to filter, save as int array
              print('What graphs to filter? (0 for nothing, seperate with ,)')
              graphs_to_filter = input()
              graphs_to_filter = np.array(graphs_to_filter.split(','), dtype=int)

              # save filtered data to new DataFrame
              filtered_data = track_data[~track_data.particle.isin(graphs_to_filter)]

              # show plots again
              plot_msd(filtered_data, 'Plot after filtering')
              if input('is it good? y/n ') == 'y':
                     break


       # remove drift #
       ################
       drift = tp.compute_drift(filtered_data)
       # show drift for each axis
       drift.plot(title='drift for each axis at each frame', ylabel='drift')
       plt.show()

       # subtract the drift
       if input('is there drift? y/n ') == 'y':
              filtered_data = tp.subtract_drift(filtered_data, drift)
              drift = tp.compute_drift(filtered_data)
              drift.plot(title='drift for each axis - after subtraction', ylabel='drift')
              plt.show()

       if input('save to new xlsx file? y/n ') == 'y':
              filtered_data.to_excel(file_path[:-17] + '_no_drift.xlsx')

if __name__ == "__main__":
       main()