#!/bin/bash
date
set -o xtrace
PS4='${LINENO}: '

cut -c1-4 < arquivo_referencia/pi-1M.txt > entradas/00-pi-2.txt
cut -c1-7 < arquivo_referencia/pi-1M.txt > entradas/01-pi-5.txt
cut -c1-12 < arquivo_referencia/pi-1M.txt > entradas/02-pi-10.txt
cut -c1-22 < arquivo_referencia/pi-1M.txt > entradas/03-pi-20.txt
cut -c1-52 < arquivo_referencia/pi-1M.txt > entradas/04-pi-50.txt
cut -c1-102 < arquivo_referencia/pi-1M.txt > entradas/05-pi-100.txt
cut -c1-202 < arquivo_referencia/pi-1M.txt > entradas/06-pi-200.txt
cut -c1-502 < arquivo_referencia/pi-1M.txt > entradas/07-pi-500.txt
cut -c1-1002 < arquivo_referencia/pi-1M.txt > entradas/08-pi-1000.txt
cut -c1-2002 < arquivo_referencia/pi-1M.txt > entradas/09-pi-2000.txt
cut -c1-5002 < arquivo_referencia/pi-1M.txt > entradas/10-pi-5000.txt
cut -c1-10002 < arquivo_referencia/pi-1M.txt > entradas/11-pi-10000.txt
cut -c1-20002 < arquivo_referencia/pi-1M.txt > entradas/12-pi-20000.txt
cut -c1-50002 < arquivo_referencia/pi-1M.txt > entradas/13-pi-50000.txt
cut -c1-100002 < arquivo_referencia/pi-1M.txt > entradas/14-pi-100000.txt
cut -c1-200002 < arquivo_referencia/pi-1M.txt > entradas/15-pi-200000.txt
cut -c1-300002 < arquivo_referencia/pi-1M.txt > entradas/16-pi-300000.txt
cut -c1-400002 < arquivo_referencia/pi-1M.txt > entradas/17-pi-400000.txt
cut -c1-500002 < arquivo_referencia/pi-1M.txt > entradas/18-pi-500000.txt
cut -c1-600002 < arquivo_referencia/pi-1M.txt > entradas/19-pi-600000.txt
cut -c1-700002 < arquivo_referencia/pi-1M.txt > entradas/20-pi-700000.txt
cut -c1-800002 < arquivo_referencia/pi-1M.txt > entradas/21-pi-800000.txt
cut -c1-900002 < arquivo_referencia/pi-1M.txt > entradas/22-pi-900000.txt
cut -c1-1000002 < arquivo_referencia/pi-1M.txt > entradas/23-pi-1000000.txt

