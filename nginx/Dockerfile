
#download the nginx image
FROM nginx:latest

#remove the default configuration
RUN rm /etc/nginx/conf.d/default.conf

#add our configuration
COPY nginx.conf /etc/nginx/conf.d/

COPY imse_ridesharing.key /etc/nginx/
COPY imse_ridesharing.crt /etc/nginx/