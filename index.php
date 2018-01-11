<html>
  <head>
    <title>WeRelate Toolkit</title>
  </head>
  <body>
    <?php
       require( dirname( __FILE__ ) . '/db.php' );
       require( dirname( __FILE__ ) . '/rss.php' );
       require( dirname( __FILE__ ) . '/main.php' );
       ?>
    <address>
      <?php print "server = ".$_SERVER['SERVER_NAME']; ?>
    </address>
  </body>
</html>
