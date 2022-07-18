#!/bin/bash

celery -A config worker -l DEBUG -c 4