FROM alpine:3.7
RUN apk --no-cache add vsftpd

COPY start_vsftpd.sh /bin/start_vsftpd.sh
COPY vsftpd.conf /etc/vsftpd/vsftpd.conf
RUN chmod +x /bin/start_vsftpd.sh

EXPOSE 21 21000-21010
VOLUME /ftp/ftp

CMD "/bin/start_vsftpd.sh"
