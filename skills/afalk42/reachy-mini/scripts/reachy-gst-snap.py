#!/usr/bin/env python3
"""Capture a single frame from Reachy Mini via GStreamer WebRTC (local).

Must run ON the robot with GST_PLUGIN_PATH set to /opt/gst-plugins-rs/lib/aarch64-linux-gnu/gstreamer-1.0
"""

import os
import sys
import time
from threading import Thread

import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GstApp, GLib
import numpy as np
from PIL import Image

OUTPUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/reachy_snap.jpg"
PRODUCER_ID = sys.argv[2] if len(sys.argv) > 2 else ""
SIGNAL_URI = sys.argv[3] if len(sys.argv) > 3 else "ws://127.0.0.1:8443"
TIMEOUT = 15


def main():
    Gst.init(None)

    loop = GLib.MainLoop()
    thread = Thread(target=loop.run, daemon=True)
    thread.start()

    pipeline = Gst.Pipeline.new("snap")
    bus = pipeline.get_bus()
    bus.add_watch(GLib.PRIORITY_DEFAULT, on_bus_message, loop)

    # Create webrtcsrc
    webrtcsrc = Gst.ElementFactory.make("webrtcsrc")
    if not webrtcsrc:
        print("ERROR: webrtcsrc not found. Set GST_PLUGIN_PATH=/opt/gst-plugins-rs/lib/aarch64-linux-gnu/gstreamer-1.0")
        return 1

    signaller = webrtcsrc.get_property("signaller")
    signaller.set_property("uri", SIGNAL_URI)
    if PRODUCER_ID:
        signaller.set_property("producer-peer-id", PRODUCER_ID)

    # Create appsink for video frames
    appsink = Gst.ElementFactory.make("appsink")
    appsink.set_property("drop", True)
    appsink.set_property("max-buffers", 1)
    caps = Gst.Caps.from_string("video/x-raw,format=BGR")
    appsink.set_property("caps", caps)

    pipeline.add(webrtcsrc)
    pipeline.add(appsink)

    # Handle dynamic pads from webrtcsrc
    def on_pad_added(src, pad):
        name = pad.get_name()
        print(f"Pad added: {name}")

        if name.startswith("video"):
            queue = Gst.ElementFactory.make("queue")
            videoconvert = Gst.ElementFactory.make("videoconvert")
            videoscale = Gst.ElementFactory.make("videoscale")

            pipeline.add(queue)
            pipeline.add(videoconvert)
            pipeline.add(videoscale)

            pad.link(queue.get_static_pad("sink"))
            queue.link(videoconvert)
            videoconvert.link(videoscale)
            videoscale.link(appsink)

            queue.sync_state_with_parent()
            videoconvert.sync_state_with_parent()
            videoscale.sync_state_with_parent()
            appsink.sync_state_with_parent()
            print("Video pipeline linked")

        elif name.startswith("audio"):
            # Discard audio - link to fakesink
            fakesink = Gst.ElementFactory.make("fakesink")
            pipeline.add(fakesink)
            pad.link(fakesink.get_static_pad("sink"))
            fakesink.sync_state_with_parent()

    webrtcsrc.connect("pad-added", on_pad_added)

    # Start pipeline
    pipeline.set_state(Gst.State.PLAYING)
    print("Pipeline playing, waiting for frame...")

    # Pull frames
    frame_captured = False
    for i in range(TIMEOUT * 5):  # 5 attempts per second
        sample = appsink.try_pull_sample(200_000_000)  # 200ms timeout
        if sample:
            buf = sample.get_buffer()
            caps_struct = sample.get_caps().get_structure(0)
            width = caps_struct.get_int("width")[1]
            height = caps_struct.get_int("height")[1]
            
            data = buf.extract_dup(0, buf.get_size())
            frame = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
            
            img = Image.fromarray(frame[..., ::-1])  # BGR -> RGB
            img.save(OUTPUT, quality=85)
            size = os.path.getsize(OUTPUT)
            print(f"Captured: {width}x{height}, saved {OUTPUT} ({size:,} bytes)")
            frame_captured = True
            break

    pipeline.set_state(Gst.State.NULL)
    loop.quit()

    if frame_captured:
        print("SUCCESS")
        return 0
    print("FAILED - no frame captured")
    return 1


def on_bus_message(bus, msg, loop):
    t = msg.type
    if t == Gst.MessageType.ERROR:
        err, debug = msg.parse_error()
        print(f"BUS ERROR: {err} / {debug}")
    elif t == Gst.MessageType.WARNING:
        warn, debug = msg.parse_warning()
        print(f"BUS WARN: {warn}")
    return True


if __name__ == "__main__":
    sys.exit(main())
