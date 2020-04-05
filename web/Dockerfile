FROM node

COPY ./ /covid-county-frontend
WORKDIR /covid-county-frontend

RUN yarn build
RUN yarn global add serve
CMD serve -s build