FROM ibmcom/websphere-traditional:latest
# chnage this to download this ojdbc8.jar , pdjrte.zip and  InetAddressInfoTest.ear from Artifactory
COPY --chown=was:root ojdbc8.jar /opt/IBM/WebSphere/AppServer/lib
COPY --chown=was:root was-jvm-config-001.props /work/config/
COPY --chown=was:root deploy.py /work/
COPY --chown=was:root pdjrte.zip /work
COPY --chown=was:root InetAddressInfoTest.ear /work
RUN cd /work && unzip pdjrte.zip
RUN /work/configure.sh /work/deploy.py
ENV PATH="/opt/IBM/WebSphere/AppServer/java/8.0/bin:/work/pdjrte/sbin:$PATH"
RUN echo $PATH
RUN java -version
# put the Tivoli jars on the classpath
RUN pdjrtecfg -action config -host docker.for.mac.host.internal -java_home /opt/IBM/WebSphere/AppServer/java/8.0/jre -cfgfiles_path /opt/IBM/WebSphere/AppServer/tivoli/tam -alt_config -config_type standalone -port 7135
