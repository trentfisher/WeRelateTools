<?php

Class DB
{
    var $servername = "localhost";
    var $dbname   = "wrt";
    var $username = "root";
    var $password = "";
    var $conn;
    
    function DB()
    {
        print "init db object";
        $this->connect();
        //$this->setup();
    }

    function connect()
    {
        try {
            $this->conn = new PDO("mysql:host=".
                                  $this->servername.
                                  ";dbname=".
                                  $this->dbname,
                                  $this->username, $this->password);
            // set the PDO error mode to exception
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            echo "Connected successfully";
        }
        catch(PDOException $e)
        {
            echo "Connection failed: " . $e->getMessage();
        }
    }

    function setup()
    {
        $schema = "";
        try
        {
            $this->conn->exec($schema);
        }
        catch(PDOException $e)
        {
            echo "Connection failed: " . $e->getMessage();
        }
    }

    function namespace2id($namespace)
    {
        // TBD cache in memory... this table should be small and almost never change
            
        // try to fetch value first
        $stmt = $this->conn->prepare(
            'SELECT id from namespace where name = :ns');
        $stmt->bindParam(':ns',  $namespace);
        $result = $stmt->execute();

        if ($stmt->rowCount() < 1)
        {
            $stmt = $this->conn->prepare(
                'INSERT INTO namespace (name) VALUES (:ns)');
            $stmt->bindParam(':ns',  $namespace);
            $stmt->execute();
            return $this->conn->lastInsertId("id");
        }
        $result = $stmt->fetch();
        $nsid = $result['id'];
        return $nsid;    
    }

    // add page to page table... update time if it already exists
    function updatepage($pagename, $updtm = "NOW")
    {
        $spn = explode(":", $pagename, 2);
        try
        {
            // if I was more clever I could probably do this as a subquery
            $nsid = $this->namespace2id($spn[0]);
            print "namespace ".$spn[0]." => ".$nsid."\n";
            
            $tmobj = new DateTime($updtm);
                
            // now update/insert page entry
            $stmt = $this->conn->prepare(
                'INSERT INTO page (namespace,name,updtm) '.
                'VALUES (:ns, :name, :updtm) '.
                'ON DUPLICATE KEY UPDATE updtm = :updtm'
            );
            $stmt->bindParam(':ns',   $nsid);
            $stmt->bindParam(':name', $spn[1]);
            $stmt->bindParam(':updtm',$tmobj->format("Y-m-d H:i:s"));
            $stmt->execute();
        }
        catch(PDOException $e)
        {
            echo "Error: " . $e->getMessage();
        }
    }

    function name2url($ns, $name)
    {
        $name = preg_replace("/\s/", "_", $name);
        return "https://www.werelate.org/wiki/".$ns.":".$name."?action=raw";
    }

    // fetch the contents of the given page and create db entries
    function fetch($ns, $name)
    {
        print "<br>TBD fetch $ns:$name\n";
        $stuff = file_get_contents($this->name2url($ns, $name));
        print "<pre>".$stuff."</pre>\n";
    }

    function fetchnext($howmany = 1)
    {
        $stmt = $this->conn->prepare(
            "SELECT namespace.name,page.name FROM page,namespace WHERE updtm > fetchtm AND page.namespace = namespace.id ORDER BY page.id LIMIT :howmany");
        $stmt->bindParam(':howmany', $howmany, PDO::PARAM_INT);
        $stmt->execute();
        //foreach ($stmt as $row)
        while ($row = $stmt->fetch())
        {
            print_r($row);
            $this->fetch($row[0], $row[1]);
        }
    }
        
    // TBD obsolete?
    function add($pagename)
    {
        $spn = explode(":", $pagename, 2);
        try
        {
            $stmt = $this->conn->prepare(
                'INSERT INTO page VALUES (:ns, :name)');
            $stmt->bindParam(':ns',  $spn[0]);
            $stmt->bindParam(':name',$spn[1]);
            $stmt->bindParam(':url', $url);
            $stmt->execute();
        }
        catch(PDOException $e)
        {
            echo "Error: " . $e->getMessage();
        }
    }
        
    // generate a bunch of data about the database
    function stats()
    {
        print "<p>Total pages:  ";
        foreach ($this->conn->query('SELECT count(*) FROM page') as $row)
        {
            print $row[0];
        }
        // how many of each kind of page?
        print "<p>Totals per namespace: ";
        print "<table>";
        foreach ($this->conn->query(
            'SELECT namespace.name, count(namespace.name) FROM page, namespace WHERE namespace.id = page.namespace group by namespace.id') as $row)
        {
            printf("<tr><td>%s</td><td>%d</td></tr>\n", $row[0],$row[1]);
        }
        print "</table>";
    }
}
?>