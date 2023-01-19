#!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils

import argparse
import sys

from poker_role import PokerRole as PR

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video output object 
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
	
# load the object detection network
# net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
# changed 
net = jetson.inference.detectNet(argv=['--model=/home/sysjetson/jetson-inference/python/training/detection/ssd/models/trump/ssd-mobilenet.onnx', '--labels=/home/sysjetson/jetson-inference/python/training/detection/ssd/models/trump/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'])

# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)

# Poker roles to display
str_role = [ "ROYAL FLUSH (1)",
			 "STRAIGHT FLUSH (2)",
			 "FOUR OF A KIND (3)",
			 "FULL HOUSE (4)",
			 "FLUSH (5)",
			 "STRAIGHT (6)",
			 "THREE OF A KIND (7)",
			 "TWO PAIR (8)",
			 "PAIR (9)",
			 "NO PAIR (10)" ]


# process frames until the user exits
pr = PR()
while True:
	# capture the next image
	img = input.Capture()

	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)

	# print the detections
	print("detected {:d} objects in image".format(len(detections)))

	cards = []
	for detection in detections:
		# print(detection)
		if detection.ClassID >= 1 and detection.ClassID <= 39:
			# club_## / diamond_## / heart_##
			cards.append(detection.ClassID - 1)
		elif detection.ClassID == 40:
			# joker
			cards.append(52)
		elif detection.ClassID >= 41 and detection.ClassID <= 53:
			# spade_##
			cards.append(detection.ClassID - 2)

	# Determine a poker role
	print("Cards (Number) :", cards)
	role = pr.check_role_main(cards)
	print("Porker Role :", str_role[role])

	# render the image
	output.Render(img)

	# update the title bar
	output.SetStatus("{:s} | Network {:.0f} FPS {:s} {:s}".format(opt.network, net.GetNetworkFPS(), 'Porker Role :', str_role[role]))

	# print out performance info
	net.PrintProfilerTimes()

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break

