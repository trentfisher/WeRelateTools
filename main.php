<?php
$db = new DB();

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
        $max = (isset($_GET["count"]) ? $_GET["count"] : "10");
        while ($max--)
        {
            $db->fetchnext();
        }
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
?>
