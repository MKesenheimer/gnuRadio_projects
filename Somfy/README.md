# Project to demodulate and decode Somfy remote control signals

- Somfy io homecontrol signals are OOK decoded
- the signal is divided over three channels at a center frequency of 868.949MHz
- the three channels are 19.2kHz (baudrate) apart
- the bitstream starts with a synchronization sequence of alternating ones and zeros
- after the synchronizations sequence, nine ones follow, after that the payload starts

...10101010111111111xxxx

- the payload is 288 symbols or 32 byte long
- most of the payload start with the sequence 0x6643
