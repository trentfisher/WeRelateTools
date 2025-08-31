<?php
$db = new DB();
Page::$DB = $db->conn;

date_default_timezone_set('America/New_York');

if (isset($_GET["action"]))
{
    if ($_GET["action"] == "rss")
    {
        fetchrss($db);
    }
    if ($_GET["action"] == "add")
    {
        # is it a url or a page name?
        $db->add($_GET["page"]);
    }
    if ($_GET["action"] == "crawl")
    {
        $max = (isset($_GET["count"]) ? $_GET["count"] : 1);
        $db->fetchnext($max);
    }
}
else
{
?>
    <p>werelate tools:
    <a href="?action=rss">fetch rss</a>
    <a href="?action=crawl">crawl</a>
    </p>
<form>
    Page: <input type="text" name="page">
    <input type="hidden" name="action" value="add">
    <input type="submit">
</form>
    Summary:
<?php
$db->stats();
}
print "\n";
$p = new Page("Person:Wilford Way (1)");
print "\n";
$p = new Person("Person:Wilford Way (1)");
print("person = <pre>".htmlspecialchars(print_r($p, true))."</pre>");
//$p->traverse_anc();

?>
