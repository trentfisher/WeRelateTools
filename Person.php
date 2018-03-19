<?php

class Person extends Page
{
    var $given;
    var $surname;
    var $gender;
    var $child_of_family;
    var $spouse_of_family;
    var $event_fact;
    
    function __construct($fn, $force = 0)
    {
        parent::__construct($fn);
        print "new Person $fn -> $this->namespace $this->name\n<br/>";

        // fetch the page if needed
        if (! $this->indb() || $force || $this->lastupd > $this->lastfetch)
        {
            $this->fetch();
            $f = $this->factsxml;
            $this->given = (string)$f->name->attributes()->given;
            $this->surname = (string)$f->name->attributes()->surname;
            $this->gender = (string)$f->gender;
            $this->child_of_family =
                (string)$f->child_of_family->attributes()->title;
        }
        if ($force || $lastupd > $lastfetch)
        {
            // update record
        }
        else
        {
            // insert new record
        }
    }
    function indb()
    {
        self::$DB->prepare(
            "SELECT * FROM person,page WHERE page.id = person.pageid AND page.name = :pagename:");

        return false;
    }
    function updatedb()
    {
        //parent to insert page
        self::$DB->prepare("INSERT INTO person (pagename, surname, given) VALUES (:pagename)");
    }
    function child_of_family()
    {
        if (!$this->child_of_family) 
        {
            return false;
        }
        if (is_string($this->child_of_family))
        {
            $this->child_of_family = new Family("Family:".$this->child_of_family);
        }
        return $this->child_of_family;
    }
    function traverse_anc()
    {
        printf("<li>%s %s\n", $this->given, $this->surname);
        $this->child_of_family() &&
            $this->child_of_family()->traverse_anc();
    }
}
?>