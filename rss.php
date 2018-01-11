<?php
// fetch rss from werelate
function fetchrss($db)
{
   $i = 0; // counter
   $url = "https://www.werelate.org/w/index.php?title=Special:Recentchanges&feed=rss"; // url to parse
   $rss = simplexml_load_file($url); // XML parser

   // RSS items loop
   // channel title + img with src
   print '<h2><img style="vertical-align: middle;" src="'.
       $rss->channel->image->url.'" /> '.
       $rss->channel->title.'</h2>';
   print '<ul>';

   foreach($rss->channel->item as $item) {
           print '<li><a href="'.$item->link.'">'.$item->title.'</a></li>';
           $db->updatepage($item->title, $item->pubDate);
   }
   print '</ul>';
}
?>
