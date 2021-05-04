#!/bin/sh
rm -r prebundle
npm run-script build
mv build prebundle
