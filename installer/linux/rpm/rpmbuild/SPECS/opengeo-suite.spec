Name: opengeo-suite
Version: 2.3.0
Release: opengeo
Summary: Allows the creation, sharing, and collaborative use of geospatial data.
License: see http://opengeo.org
Requires(post): bash
Requires(preun): bash
Requires: opengeo-geoserver

%define _rpmdir ../
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define _unpackaged_files_terminate_build 0

%description
At its core, the opengeo-suite has a stack based on GeoServer,
Django, and GeoExt that provides a platform for sophisticated
web browser spatial visualization and analysis. Atop this stack,
the project has built a map composer and viewer, tools for
analysis, and reporting tools.


%install
        rm -rf $RPM_BUILD_ROOT
        mkdir -p $RPM_BUILD_ROOT/usr/share/opengeo-suite
        mkdir -p $RPM_BUILD_ROOT/var/lib/tomcat5/webapps

        cp -rp $RPM_SOURCE_DIR/opengeo-suite/dashboard.war $RPM_BUILD_ROOT/var/lib/tomcat5/webapps/.
        cp -rp $RPM_SOURCE_DIR/opengeo-suite/geoeditor.war $RPM_BUILD_ROOT/var/lib/tomcat5/webapps/.
        cp -rp $RPM_SOURCE_DIR/opengeo-suite/geowebcache.war $RPM_BUILD_ROOT/var/lib/tomcat5/webapps/.
        cp -rp $RPM_SOURCE_DIR/opengeo-suite/recipes.war $RPM_BUILD_ROOT/var/lib/tomcat5/webapps/.
        cp -rp $RPM_SOURCE_DIR/opengeo-suite/geoexplorer.war $RPM_BUILD_ROOT/var/lib/tomcat5/webapps/.

        unzip $RPM_SOURCE_DIR/opengeo-suite/geoexplorer.war -d $RPM_BUILD_ROOT/geoexplorer
        cp $RPM_SOURCE_DIR/opengeo-suite/debian/web.xml $RPM_BUILD_ROOT/geoexplorer/WEB-INF/web.xml
        ( cd $RPM_BUILD_ROOT/geoexplorer ; zip ../geoexplorer.zip * -r ; cd ..)
        cp -rp $RPM_BUILD_ROOT/geoexplorer.zip $RPM_BUILD_ROOT/var/lib/tomcat5/webapps/geoexplorer.war
        rm -rf $RPM_BUILD_ROOT/geoexplorer $RPM_BUILD_ROOT/geoexplorer.zip
	cp -rp $RPM_SOURCE_DIR/scripts/opengeo-setup.sh $RPM_BUILD_ROOT/usr/share/opengeo-suite/.
%post
	echo "OPENGEO: you will need to run /usr/share/opengeo-suite/opengeo-setup.sh to complete this installation"

%preun
# stop services

        if [ -e /var/lib/tomcat5/webapps/geoexplorer ]; then
                invoke-rc.d tomcat5 stop
                rm -rf /var/lib/tomcat5/webapps/recipes /var/lib/tomcat5/webapps/dashboard
                rm -rf /var/lib/tomcat5/webapps/geoeditor /var/lib/tomcat5/webapps/geowebcache
                rm -rf /var/lib/tomcat5/webapps/geoexplorer /var/lib/tomcat5/webapps/geowebcache
                rm -rf /var/lib/tomcat5/webapps/dashboard.war
                rm -rf /var/lib/tomcat5/webapps/geoeditor.war
                rm -rf /var/lib/tomcat5/webapps/geoexplorer.war
                rm -rf /var/lib/tomcat5/webapps/geowebcache.war
                rm -rf /var/lib/tomcat5/webapps/recipes.war
                service tomcat5 start
        fi

%postun
# remove files
# remove users


%clean

%files
%defattr(-,root,root,-)
%dir "/var/lib/tomcat5/webapps/*"
/usr/share/opengeo-suite/opengeo-setup.sh