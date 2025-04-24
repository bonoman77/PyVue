index_chart = {
    initDashboardPageCharts: function(){

        if( $('#serviceTimeChart').length != 0 && $('#bibleStudyChart').length != 0 ){
            /* ----------==========     Daily Sales Chart initialization    ==========---------- */

            dataServiceTimeChart = {
              labels: ['9', '10', '11', '12', '1', '2', '3', '4', '5', '6', '7', '8'],
              series: [
                hours_data
              ]
            };

            optionsServiceTimeChart = {
                lineSmooth: Chartist.Interpolation.cardinal({
                    tension: 0
                }),
                low: 0,
                high: hours_max, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
                chartPadding: { top: 0, right: 0, bottom: 0, left: 0},
            }

            var serviceTimeChart = new Chartist.Line('#serviceTimeChart', dataServiceTimeChart, optionsServiceTimeChart);

            md.startAnimationForLineChart(serviceTimeChart);


            dataBibleStudyChart = {
              labels: ['9', '10', '11', '12', '1', '2', '3', '4', '5', '6', '7', '8'],
              series: [
                study_data
              ]
            };

            optionsBibleStudyChart = {
                lineSmooth: Chartist.Interpolation.cardinal({
                    tension: 0
                }),
                low: 0,
                high: study_max, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
                chartPadding: { top: 0, right: 0, bottom: 0, left: 0},
            }

            var bibleStudyChart = new Chartist.Line('#bibleStudyChart', dataBibleStudyChart, optionsBibleStudyChart);

            md.startAnimationForLineChart(bibleStudyChart);

        }
    }
}


pub_chart = {
    initDashboardPageCharts: function(){

        if( $('#serviceTimeChart').length != 0 && $('#bibleStudyChart').length != 0 ){
            /* ----------==========     Daily Sales Chart initialization    ==========---------- */

            dataServiceTimeChart = {
              labels: month_data,
              series: [
                hours_data
              ]
            };

            optionsServiceTimeChart = {
                lineSmooth: Chartist.Interpolation.cardinal({
                    tension: 0
                }),
                low: 0,
                high: hours_max, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
                chartPadding: { top: 0, right: 0, bottom: 0, left: 0},
            }

            var serviceTimeChart = new Chartist.Line('#serviceTimeChart', dataServiceTimeChart, optionsServiceTimeChart);

            md.startAnimationForLineChart(serviceTimeChart);


            dataBibleStudyChart = {
              labels: month_data,
              series: [
                study_data
              ]
            };

            optionsBibleStudyChart = {
                lineSmooth: Chartist.Interpolation.cardinal({
                    tension: 0
                }),
                low: 0,
                high: study_max, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
                chartPadding: { top: 0, right: 0, bottom: 0, left: 0},
            }

            var bibleStudyChart = new Chartist.Line('#bibleStudyChart', dataBibleStudyChart, optionsBibleStudyChart);

            md.startAnimationForLineChart(bibleStudyChart);

        }
    }
}


