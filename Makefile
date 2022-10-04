
vayyar-factory-reset:
	@echo "resetting vayyar to factory setting, please hold top buttom while unplugging and replugging power..."
	@python -m esptool erase_region 0xa000 0xFF6000

vayyar-erase-provision-only:
	@echo "erase provision data..."
	@python -m esptool erase_region 0xa000 0x3000

vayyar-flash-vblu-factory:
	@echo "flash factory data to flash..."
	@python ./script/flash_factory_data.py WH2BAUS01 BLUGBC0Q013S00000000000000000001 VXTAA2013S0000000000000000000001 1 2

vayyar-flash-application:
	@echo "flashing v36 application to flash..."
	@python -m esptool -b 921600 --after hard_reset write_flash --flash_mode dio --flash_size 16MB --flash_freq 40m 0x1000 bin/bootloader.bin 0x8000 bin/partition-table.bin 0xd000 bin/ota_data_initial.bin 0x10000 bin/walabot-home-vblu.bin

vayyar-usb-log:
	@echo "start usb log mode..."
	@script -a -t 0 out27.txt screen /dev/tty.usbserial-DO02K4IH 115200
