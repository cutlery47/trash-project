FROM redis:7.2.5-alpine

USER root

COPY entry.sh /entry.sh
COPY redis.conf /usr/local/etc/redis/redis.conf

RUN mkdir /var/run/redis/
RUN chmod 777 /var/run/redis/
RUN chmod +x /entry.sh

CMD ["/entry.sh"]
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]

#TODO: create a compose file in order to connect all the services by a single network
