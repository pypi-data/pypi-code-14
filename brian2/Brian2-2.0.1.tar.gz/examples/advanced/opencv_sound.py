import os
import urllib2
import cv2  # Import OpenCV2
import cv2.cv as cv  # Import the cv subpackage, needed for some constants

from brian2 import *

defaultclock.dt = 1*ms
# prefs.codegen.target = 'weave'
# prefs.logging.std_redirection = False
set_device('cpp_standalone')
filename = os.path.abspath('Megamind.avi')

if not os.path.exists(filename):
    print('Downloading the example video file')
    response = urllib2.urlopen('http://docs.opencv.org/2.4/_downloads/Megamind.avi')
    data = response.read()
    with open(filename, 'wb') as f:
        f.write(data)

video = cv2.VideoCapture(filename)
width, height, frame_count = (int(video.get(cv.CV_CAP_PROP_FRAME_WIDTH)),
                              int(video.get(cv.CV_CAP_PROP_FRAME_HEIGHT)),
                              int(video.get(cv.CV_CAP_PROP_FRAME_COUNT)))
fps = 24
time_between_frames = 1*second/fps

# Links the necessary libraries
prefs.codegen.cpp.libraries += ['opencv_core',
                                'opencv_highgui']

# Includes the header files in all generated files
prefs.codegen.cpp.headers += ['<opencv2/core/core.hpp>',
                              '<opencv2/highgui/highgui.hpp>']

# Pass in values as macros
# Note that in general we could also pass in the filename this way, but to get
# the string quoting right is unfortunately quite difficult
prefs.codegen.cpp.define_macros += [('VIDEO_WIDTH', width),
                                    ('VIDEO_HEIGHT', height),
                                    ('FILTER_SIZE', 50)]
@implementation('cpp', '''
double* _get_frame(double t)
{
    // The following initializations will only be executed once
    static cv::VideoCapture source("VIDEO_FILENAME");
    static cv::Mat frame;
    static double* grayscale_frame = (double*)malloc(VIDEO_WIDTH*VIDEO_HEIGHT*sizeof(double));
    static double last_update = -1.;
    if (t > last_update)
    {
        source >> frame;
        for (int row=0; row<VIDEO_HEIGHT; row++)
            for (int col=0; col<VIDEO_WIDTH; col++)
            {
                const double grayscale_value = (frame.at<cv::Vec3b>(row, col)[0] +
                                                frame.at<cv::Vec3b>(row, col)[1] +
                                                frame.at<cv::Vec3b>(row, col)[2])/(3.0*128);
                grayscale_frame[row*VIDEO_WIDTH + col] = grayscale_value;
            }
        last_update = t;
    }
    return grayscale_frame;
}

double spatial_response(const double t, const int x, const int y)
{
    const double *frame = _get_frame(t);
    double sum = 0.0;
    for (int pos_x = max(0, x - FILTER_SIZE/2); pos_x < min(VIDEO_WIDTH, x + FILTER_SIZE/2); pos_x++)
        for (int pos_y = max(0, y - FILTER_SIZE/2); pos_y < min(VIDEO_HEIGHT, y + FILTER_SIZE/2); pos_y++)
        {
            const double filter = 17/(5.0*5.0)*exp(pow((x - pos_x)/5, 2)) - 16/(20.*20.)*exp(pow((x - pos_x)/20, 2));
            sum += frame[pos_y*VIDEO_WIDTH + pos_x] * filter;
        }
    return sum/(FILTER_SIZE/2);
}
'''.replace('VIDEO_FILENAME', filename))
@check_units(t=second, x=1, y=1, result=1)
def spatial_response(t, x, y):
    raise NotImplementedError('Use a C++-based code-generation target')



# Two layers
#   LGN = Poisson neurons, rate = filter (write as custom function)
#   V1  = I & F neurons, connected reasonably

# LGN : On and Off cells
N_LGN = width * height
tau = 10*ms
LGN = NeuronGroup(N_LGN, '''
drate/dt = (s - rate)/tau : Hz
ds/dt = -spatial/tau : Hz
spatial = on_off * spatial_response(t, x, y) * 10*Hz : Hz
x : 1 (constant)
y : 1 (constant)
on_off : integer (constant)
preferred_sf : 1 (constant)
''', threshold='rand()<rate*dt')
LGN.x = 'i%width'
LGN.y = 'i/width'
LGN.on_off = 1

mon = SpikeMonitor(LGN)
runtime = frame_count*defaultclock.dt
run(runtime, report='text')
