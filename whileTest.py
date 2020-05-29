
while True:
	
	command = input("enter a command:\n")
    command = int(command)

	while True:
	    spi.xfer2(0x7e)
	    if KeyboardInterupt:
	        break
    # SPI code