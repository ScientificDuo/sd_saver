#! python
"""

  A simple program that just downloads images from a remote server and saves as png.  It needs some additional tweaks however it works for now.
 
 Examples:
  sd_saver.py --url "http://magma.vsi.esdm.go.id/img/sgramsekarang/AGU.png" --freq=300 --output_dir "<location>/Agung/Spectrogram" --filename "Agung_Spectrogram_"
  sd_saver.py --url "https://magma.vsi.esdm.go.id/img/wf/TMKS.png" --freq=300 --output_dir "<location>/Agung/Webicorder" --filename "Agung_Webicorder_"
"""


from io import BytesIO
from PIL import Image
from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
from datetime import datetime
import requests
import time 
import pytz


__author__ = "@ScientificDuo"
__copyright__ = "Copyright 2017, The Scientific Duo"
__license__ = ""
__version__ = "1.0.0"
__status__ = "Production"

					
def main():
	parser = ArgumentParser(prog='sd_saver', description='The Scientific Duo image saving utility',formatter_class=ArgumentDefaultsHelpFormatter)
	parser.add_argument('-u', '--url', type=str, required=True, help='The remote url of image, ex. https://magma.vsi.esdm.go.id/img/wf/TMKS.png')
	parser.add_argument('-o', '--output_dir', type=str, required=True,  help='Output directory files will be saved to.')
	parser.add_argument('-n', '--filename', type=str, required=True, help='Name of the output filename')
	parser.add_argument('-f', '--freq', type=int, required=False, help='How often should the program fetch for the image in seconds',default=300)
	parser.add_argument('-t', '--time_format', type=str, required=False, default='%Y-%m-%dT%H.%M.%S', help='The format of the timestamp, iso like format is default and recommended')
	parser.add_argument('-z', '--timezone', type=str, required=False, default='Australia/Perth', help='Timezone to use. If left blank local machine timezone will be used. pytz list')
		
	# parse the arguments
	args = parser.parse_args()

	while True:
		try:
			#Get save times and convert to passed timezome
			utc_dt = datetime.now(pytz.utc)
			tz = pytz.timezone(args.timezone)
			dt = utc_dt.astimezone(tz)
			
			#Format for output into filename
			final_dt = dt.strftime(args.time_format)
			
			#Pull the resouce from the URL provided
			r = requests.get(args.url)
			i = Image.open(BytesIO(r.content))
			
			#Save to disk with concatenation of name and datetime
			i.save(args.output_dir + "/" + args.filename + final_dt + ".png")
			print("File Saved:" + args.output_dir + "/" + args.filename +  final_dt + ".png")
			
			#Wait the required seconds before attempting again
			time.sleep(args.freq)
			
		except OSError as err:
			#Sometimes the download fails, just print the message and try again
			print("OS Error: {0}".format(err))

			
if __name__ == '__main__':
	main()
	