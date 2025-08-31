<?php

// a generic base class for any WeRelate page

Class Page
{
    public static $DB;
    var $name;
    var $id;
    var $namespace;
    var $nsid;
    var $lastupd = 0;   // when this page was last updated on WeRelate
    var $lastfetch = 0; // when this page was last fetched from WeRelate
    var $factsxml;
    var $text;
    function __construct($fn)
    {
        // we expect something like Person:John Doe (1)
        list($this->namespace, $this->name) = $this->name2parts($fn);
        print "new Page $fn -> $this->namespace $this->name\n<br/>";
        $nsid = $this->namespace2id($this->namespace);
        if (!$this->indb())
        {
        }
    }

    function name2parts($pagename)
    {
        $spn = explode(":", $pagename, 2);
        return $spn;
    }
    function name2url($ns, $name)
    {
        $name = preg_replace("/\s/", "_", $name);
        return "https://www.werelate.org/wiki/".$ns.":".$name."?action=raw";
    }
        
    function namespace2id($namespace)
    {
        // TBD cache in memory... this table should be small and almost never change
            
        // try to fetch value first
        $stmt = self::$DB->prepare(
            'SELECT id from namespace where name = :ns');
        $stmt->bindParam(':ns',  $namespace);
        $result = $stmt->execute();

        if ($stmt->rowCount() < 1)
        {
            $stmt = self::$DB->prepare(
                'INSERT INTO namespace (name) VALUES (:ns)');
            $stmt->bindParam(':ns',  $namespace);
            $stmt->execute();
            return self::$DB->lastInsertId("id");
        }
        $result = $stmt->fetch();
        $nsid = $result['id'];
        return $nsid;
    }

    function indb()
    {
        $stmt = self::$DB->prepare(
            "SELECT * FROM page WHERE namespace = :nsid: AND name = :name:");
        $stmt->bindParam(':ns',  $nsid);
        $stmt->bindParam(':name',  $name);
        $stmt->execute();
        
        return false;

    }

    function updatedb()
    {
    }
            
    // routines for loading pages from WeRelate, used by child objects
    function splitfacts($stuff)
    {
        // Pick out the leading XML
        preg_match("((?is)^\s*<(\w+)>(.+)</\\1>(.*))",
                   $stuff, $match);
        //print("match = <pre>".htmlspecialchars(print_r($match, true))."</pre>");

        $facts = sprintf("<%s>%s</%s>", $match[1], $match[2], $match[1]);

        // clean up the remaining text
        $text = $match[3];
        preg_replace("(<show_sources_images_notes/>)", "", $text);
        preg_replace("((?s)[ \t\r\n]+$)", "", $text);
        preg_replace("((?s)^[ \t\r\n]+)", "", $text);

        return array($facts, $text);
    }
    // fetch the raw contents of the given page and return the xml object
    function fetch()
    {
        $url = $this->name2url($this->namespace, $this->name);
        print "<br>fetching $this->namespace:$this->name -> $url\n";
        $stuff = file_get_contents($url);
        //print "<pre>".htmlspecialchars($stuff)."</pre>\n";
        list($facts, $text) = $this->splitfacts($stuff);
        $this->factsxml = simplexml_load_string($facts);
        $this->text = $text;
        //print "parsed facts: <pre>".htmlspecialchars(print_r($this->factsxml, true))."</pre>\n";
    }
}

?>