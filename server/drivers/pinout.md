### Beaglebone Black RS485 Signal Pinout ###

* Transmit Enable - P9.15/GPIO_48 - When logic-1, we are transmitting. When logic-0, we are receiving.
* TX - P9.24/GPIO_15 - Transmits data out from the Beaglebone to the device UART1 -> /dev/ttyO1
* RX - P9.26/GPIO_14 - Receives data into the Beaglebone from the device on UART1 -> /dev/ttyO1
