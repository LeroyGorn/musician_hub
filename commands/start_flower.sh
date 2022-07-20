#!/bin/bash

celery -A config flower --broker=redis://redis