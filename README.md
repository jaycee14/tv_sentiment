# tv_sentiment
A deep learning nlp approach to deciding what to watch...

![Cycle Images](resources/screenshow.gif)

## Overview
My aims were:
* Train and use an NLP model in an application
* Build a Docker based application to learn how
* Find some new shows to watch!

## Architecture

![Architecture](resources/architecture_sq.jpg)

### Issuse Encountered
* At the time of writing Docker-Compose did not have GPU pass through support. Initially I ran the NLP engine in a separate docker container with GPU pass through (available in Linux) then converted the model to default to CPU. This seemed more in line with a production system where CPUs are plentiful (for scaling) and the model is only doing the forward pass.
* Persistant database storage that could be accessed outside the docker container for development.
  * This was solved be pre-defining a data volume for docker that could be mapped into the compose group or into a standalone container.

## Output

## Future Ideas

* Starlette for asynchronous web serving
* FastAPI for API development / serving
