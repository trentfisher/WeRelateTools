<?php

class Family extends Page
{
    var $name;
    var $husband;
    var $wife;

    function __construct($fn, $force = 0)
    {
        parent::__construct($fn);
        print "new Family $fn -> $this->namespace $this->name\n<br/>";

        // fetch the page if needed
        if (! $this->indb() || $force || $lastupd > $lastfetch)
        {
            $this->fetch();
            $f = $this->factsxml;
            $this->husband = (string)$f->husband->attributes()->title;
            $this->wife = (string)$f->wife->attributes()->title;
        }
    }

    function indb()
    {
        return false;
    }

    function husband()
    {
        if (!$this->husband) { return false; }
        if (is_string($this->husband))
        {
            $this->husband = new Person("Person:".$this->husband);
        }
        return $this->husband;
    }

    function wife()
    {
        if (!$this->wife) { return false; }
        if (is_string($this->wife))
        {
            $this->wife = new Person("Person:".$this->wife);
        }
        return $this->wife;
    }

    function traverse_anc()
    {
        print "<ul>\n";
        print $this->name;
        print "<br>\n";
        $this->husband() && $this->husband()->traverse_anc();
        $this->wife() && $this->wife()->traverse_anc();
        print "</ul>\n";
    }
}

?>