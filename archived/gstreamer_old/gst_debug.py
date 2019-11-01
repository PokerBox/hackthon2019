# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from PIL import Image
import warnings
warnings.filterwarnings("ignore")
from gi.repository import GLib, GObject, Gst, GstBase
import sys
from functools import partial
import svgwrite
import time

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')

X_PIXEL = 640
Y_PIXEL = 480
FRAME_RATE = 30
ROTATE_180 = True

GObject.threads_init()
Gst.init(None)


def on_bus_message(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        loop.quit()
    elif t == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        sys.stderr.write('Warning: %s: %s\n' % (err, debug))
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write('Error: %s: %s\n' % (err, debug))
        loop.quit()
    return True


def on_new_sample(sink, overlay, screen_size, appsink_size, user_function):
    sample = sink.emit('pull-sample')
    buf = sample.get_buffer()
    result, mapinfo = buf.map(Gst.MapFlags.READ)
    if result:
        img = Image.frombytes(
            'RGB', (appsink_size[0], appsink_size[1]), mapinfo.data, 'raw')
        if ROTATE_180:
            img = img.rotate(180)
        svg_canvas = svgwrite.Drawing(
            '', size=(screen_size[0], screen_size[1]))
        img.save("img1.png","PNG")
        print('image saved, sleeping 10 seconds')
        time.sleep(10)
        user_function(img, svg_canvas)
        overlay.set_property('data', svg_canvas.tostring())
    buf.unmap(mapinfo)
    return Gst.FlowReturn.OK


def detectCoralDevBoard():
    try:
        if 'MX8MQ' in open('/sys/firmware/devicetree/base/model').read():
            print('Detected Edge TPU dev board.')
            return True
    except:
        pass
    return False


def run_pipeline(user_function,
                 src_size=(X_PIXEL, Y_PIXEL),
                 appsink_size=(639, 480)):
    PIPELINE = 'v4l2src device=/dev/video1 ! {src_caps} ! {leaky_q} '
    if detectCoralDevBoard():
        SRC_CAPS = 'video/x-raw,format=YUY2,width={width},height={height},framerate={frame_rate}/1'
        PIPELINE += """ ! glupload ! tee name=t
            t. ! {leaky_q} ! glfilterbin filter=glcolorscale
               ! {dl_caps} ! videoconvert ! {sink_caps} ! {sink_element}
            t. ! {leaky_q} ! glfilterbin filter=glcolorscale
               ! rsvgoverlay name=overlay ! waylandsink
        """
    else:
        SRC_CAPS = 'video/x-raw,width={width},height={height},framerate={frame_rate}/1'
        PIPELINE += """ ! tee name=t
            t. ! {leaky_q} ! videoconvert ! videoscale ! {sink_caps} ! {sink_element}
            t. ! {leaky_q} ! videoconvert
               ! rsvgoverlay name=overlay ! videoconvert ! ximagesink
            """

    SINK_ELEMENT = 'appsink name=appsink sync=false emit-signals=true max-buffers=1 drop=true'
    DL_CAPS = 'video/x-raw,format=RGBA,width={width},height={height}'
    SINK_CAPS = 'video/x-raw,format=RGB,width={width},height={height}'
    LEAKY_Q = 'queue max-size-buffers=1 leaky=downstream'

    src_caps = SRC_CAPS.format(
        width=src_size[0], height=src_size[1], frame_rate=FRAME_RATE)
    dl_caps = DL_CAPS.format(width=appsink_size[0], height=appsink_size[1])
    sink_caps = SINK_CAPS.format(width=appsink_size[0], height=appsink_size[1])
    pipeline = PIPELINE.format(leaky_q=LEAKY_Q,
                               src_caps=src_caps, dl_caps=dl_caps, sink_caps=sink_caps,
                               sink_element=SINK_ELEMENT)

    print("Preparing streamer pipeline")
    print("Camera resolution", src_size[0],
          src_size[1], "Frame rate", FRAME_RATE)
    print(pipeline)
    pipeline = Gst.parse_launch(pipeline)
    

    overlay = pipeline.get_by_name('overlay')
    appsink = pipeline.get_by_name('appsink')
    appsink.connect('new-sample', partial(on_new_sample,
                                          overlay=overlay, screen_size=src_size,
                                          appsink_size=appsink_size, user_function=user_function))
    loop = GObject.MainLoop()

    # Set up a pipeline bus watch to catch errors.
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect('message', on_bus_message, loop)

    # Run pipeline.
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except:
        pass

    # Clean up.
    pipeline.set_state(Gst.State.NULL)
    while GLib.MainContext.default().iteration(False):
        pass
