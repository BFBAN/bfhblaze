enableFiberStackCheck = true

#ifndef BASE_PORT
    #define BASE_PORT 17500
#endif

// PLATFORM needs to be a real platform (ps3, xbl2 are currently supported)
#ifndef PLATFORM
    #define PLATFORM "pc"
#endif

//gos developer's blaze servers
#define BLAZE_SERVICE_NAME "qos-2010-#PLATFORM#-#REGION#"

#define DBHOST "gosprdmydb2a.abn-iad.ea.com"
#define DBPORT 3306

// scheduler
#define DBBASE "qos"
#define DBUSER "gos_ops"
#define DBPASS "gos_ops"
#define DBMAX 8
#define DBMIN 1
#define DBCLIENT "MYSQL"

// XLSP and Redirector configuration, you will not need to modify these settings
#define XBOX_360_SERVICE_ID "0x45410000"
#define XBOX_360_LSP_NAME ""
#define REDIRECTOR_ADDRESS "internal.gosredirector.ea.com"
#define XBOX_360_SITE_NAME_SJC "sdev-sjc"
#define XBOX_360_SITE_NAME_IAD "sdev-sjc"
#define XBOX_360_SITE_NAME_GVA "sdev-sjc"

// QoS servers
#define QOS_SERVER_NAME_SJC "python.online.ea.com"
#define QOS_SERVER_NAME_IAD "python.online.ea.com"
#define QOS_SERVER_NAME_GVA "python.online.ea.com"

#define TELEM_SERVER "10.30.80.234"

deployInfo = {
    // E-mail addresses for the monitor to notify on server crash
    monitorMail = "nobody@ea.com"

    // E-mail addresses for the monitor to notify on server crash - not restarted
    monitorNotRestartedMail = "nobody@ea.com"

    // Monitor restart threshold
    monitorAllowedCrashCount = 3
    monitorAllowedCrashTime = 10

    // E-mail addresses for deploy notification
    deployMail = "nobody@ea.com"
}

#include "blaze.boot"


