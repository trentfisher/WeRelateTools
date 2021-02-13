<?php
Class One
{
    static $foo = "NO";
    function p(){ print "foo = ".self::$foo."\n"; }
}

Class Two extends One
{
    function p(){ print "child foo = ".self::$foo."\n"; }
}

$a = new One;
$a->p();
One::$foo = "HELLO";
$a->p();
$b = new Two;
$b->p();
$c = new Two;
$c->p();
One::$foo = "ADIOS";
$a->p();
$b->p();
$c->p();

?>