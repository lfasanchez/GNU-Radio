"""
Copyright 2007, 2008, 2009 Free Software Foundation, Inc.
This file is part of GNU Radio

GNU Radio Companion is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

GNU Radio Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

import pygtk
pygtk.require('2.0')
import gtk

from Dialogs import TextDisplay
from Constants import MIN_DIALOG_WIDTH, MIN_DIALOG_HEIGHT

def get_title_label(title):
	"""
	Get a title label for the params window.
	The title will be bold, underlined, and left justified.
	@param title the text of the title
	@return a gtk object
	"""
	label = gtk.Label()
	label.set_markup('\n<b><span underline="low">%s</span>:</b>\n'%title)
	hbox = gtk.HBox()
	hbox.pack_start(label, False, False, padding=11)
	return hbox

class ParamsDialog(gtk.Dialog):
	"""A dialog box to set block parameters."""

	def __init__(self, block):
		"""
		SignalBlockParamsDialog contructor.
		@param block the signal block
		"""
		gtk.Dialog.__init__(self,
			title='Properties: %s'%block.get_name(),
			buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE),
		)
		self.block = block
		self.set_size_request(MIN_DIALOG_WIDTH, MIN_DIALOG_HEIGHT)
		vbox = gtk.VBox()
		#Add the title label
		vbox.pack_start(get_title_label('Parameters'), False)
		#Create the scrolled window to hold all the parameters
		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrolled_window.add_with_viewport(vbox)
		self.vbox.pack_start(scrolled_window, True)
		#Error Messages for the block
		self._error_box = gtk.VBox()
		self._error_messages_text_display = TextDisplay()
		self._error_box.pack_start(gtk.Label(), False, False, 7) #spacing
		self._error_box.pack_start(get_title_label('Error Messages'), False)
		self._error_box.pack_start(self._error_messages_text_display, False)
		#Docs for the block
		self._docs_box = err_box = gtk.VBox()
		self._docs_text_display = TextDisplay()
		self._docs_box.pack_start(gtk.Label(), False, False, 7) #spacing
		self._docs_box.pack_start(get_title_label('Documentation'), False)
		self._docs_box.pack_start(self._docs_text_display, False)
		#Add all the parameters
		for param in self.block.get_params():
			vbox.pack_start(param.get_input_object(self._handle_changed), False)
		#Add the error and docs box
		vbox.pack_start(self._error_box, False)
		vbox.pack_start(self._docs_box, False)
		#connect and show
		self.connect('key_press_event', self._handle_key_press)
		self.show_all()
		#initial update
		for param in self.block.get_params(): param.update()
		self._update()

	def _update(self):
		"""
		Update the error messages box.
		Hide the box if there are no errors.
		Update the documentation block.
		Hide the box if there are no docs.
		"""
		self.block.validate()
		#update the errors box
		if self.block.is_valid(): self._error_box.hide()
		else: self._error_box.show()
		messages = '\n\n'.join(self.block.get_error_messages())
		self._error_messages_text_display.set_text(messages)
		#update the docs box
		if self.block.get_doc(): self._docs_box.show()
		else: self._docs_box.hide()
		self._docs_text_display.set_text(self.block.get_doc())

	def _handle_key_press(self, widget, event):
		"""
		Handle key presses from the keyboard.
		Call the ok response when enter is pressed.
		@return false to forward the keypress
		"""
		keyname = gtk.gdk.keyval_name(event.keyval)
		if keyname == 'Return': self.response(gtk.RESPONSE_OK)
		return False #forward the keypress

	def _handle_changed(self, param):
		"""
		A change occured, update any dependent parameters:
		The enum inside the variable type may have changed and,
		the variable param will need an external update.
		@param param the graphical parameter that initiated the callback
		"""
		#update dependent params
		if param.is_enum():
			for other_param in param.get_parent().get_params():
				if param.get_key() is not other_param.get_key() and (
				param.get_key() in other_param._type or \
				param.get_key() in other_param._hide): other_param.update()
		#update
		self._update()
		return True

	def run(self):
		"""
		Call run().
		@return true if a change occured.
		"""
		original_data = list()
		for param in self.block.get_params():
			original_data.append(param.get_value())
		gtk.Dialog.run(self)
		self.destroy()
		new_data = list()
		for param in self.block.get_params():
			new_data.append(param.get_value())
		return original_data != new_data
