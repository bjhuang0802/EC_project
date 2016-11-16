<?php

    ini_set('memory_limit', '-1');
    $input = array_map('str_getcsv', file('/home/ubuntu/2501/rawdata020/input.csv'));
    $output = array("client_id,session_start,session_end,count,start_page,end_page".PHP_EOL);

    $clid_pnt = $input[0][0];
    $time_pnt = $input[0][1];
    $page_pnt = $input[0][2];
    $cnt = 1;

    for ($i=1; $i<count($input); $i++)
    {
        if(strcmp($input[$i][0],$clid_pnt)!=0 || ($input[$i][1] - $time_pnt >= 1800))
        {
            array_push($output, $clid_pnt.','.$time_pnt.','.$input[$i-1][1].','.$cnt.','.$page_pnt.','.$input[$i-1][2].PHP_EOL);
            $clid_pnt = $input[$i][0];
            $time_pnt = $input[$i][1];
            $page_pnt = $input[$i][2];
            $cnt = 0;
        }
        $cnt++;
    }

    array_push($output, $clid_pnt.','.$time_pnt.','.$input[$i-1][1].','.$cnt.','.$page_pnt.','.$input[$i-1][2].PHP_EOL);
    file_put_contents("/home/ubuntu/2501/rawdata020/output.csv", $output, LOCK_EX);

?>
