server <- function(input, output, session){

	Selected = reactive({
		selected = subset(variables, colname == input$vars)
	})

	###############################################################
	# Create descriptive table as follows:                        #
	#   1. Group data by variable in [Selected]                   #
	#   2. For each group, compute the count of rows              #
	#   3. For each group, find the average values for:           #
	#     a. Overall Score                                        #
	#     b. Potential Score                                      #
	#     c. Wage                                                 #
	#     d. Value                                                #
	# and assign the output table to [output$descriptive_table]   #
	#                                                             #
	# START CODE:                                                 #
	desc_selected = reactive({
		selected = Selected()
		col_selected = selected$colname
		if (selected$type == 'categorical'){
			selected.data = fifa[fifa[, as.character(col_selected)]!='',] 
			out = aggregate(
			  selected.data[, as.character(subset(variables, type == 'numeric')$colname)],
			  by = list(var = selected.data[, as.character(col_selected)]),
			  mean
			)
			colnames(out) = c('Var', as.character(subset(variables, type == 'numeric')$label))
			t1 = aggregate(selected.data$name, by = list(var = selected.data[, as.character(col_selected)]), length)		
			colnames(t1) = c('Var', 'Count')
			out = merge(t1, out)
			out = head(out[order(out$Count, decreasing = TRUE), ], 5)
		} else if (selected $type == 'numeric') {
			out = t(as.matrix(summary(fifa[, as.character(selected$colname)])))
		}	 		
		return(out)
	})

	output$descriptive_table  = renderTable(desc_selected())
	# END CODE                                                    #
	###############################################################

	#############################################################
	# Visualize univariate distributions:                       #
	#   * Frequency table barplot for categorical variables     #
	#   * Histogram for numerical variables                     #
	#   * Assign the renderPlot to [output$descriptive_visual]  #
  #                                                           #
	# START CODE:                                               #
	output$descriptive_visual = renderPlot({
		selected = Selected() 
		if (selected$type == 'categorical'){
			selected.data = fifa[, as.character(selected$colname)] 
			out = head(sort(table(selected.data[selected.data!='']), decreasing= TRUE), 20); 
			barplot(out, las = 1, main='Frequency Table', xlab=selected$label)
		} else if (selected $type == 'numeric') {
			out = fifa[, as.character(selected$colname)]
			hist(out, las=1, main='Histogram', xlab=selected$label, col='lightgrey')
		}
	})
	# END CODE:                                                 #
	#############################################################
	
	output$select_group = renderUI({		
	  selectInput("selected_group", "Selected Group:", choices = sort(unique(fifa[, input$groups])), multiple = TRUE, selected = NULL) 	  
	})
	
	Selected_group = reactive({
		selected_gp = input$selected_group
		if (!is.null(selected_gp)){
			out = subset(fifa, fifa[, input$groups] %in% selected_gp) 
		} else {
			out = fifa 
		}		
		return(out)
	})

	selected_summary = reactive({
		selected = Selected_group()
		if (nrow(selected) > 0){
			selected_sum = aggregate(selected[, input$target], by = list(var = selected[, as.character(input$groups)]), mean)
			colnames(selected_sum) = c(as.character(subset(variables, colname == input$groups)$label), 'Average')
			tmp = aggregate(selected[, input$target], by = list(var = selected[, as.character(input$groups)]), median)
			colnames(tmp) = c(as.character(subset(variables, colname == input$groups)$label), 'Median')
			selected_sum = merge(selected_sum, tmp)
			tmp = aggregate(selected[, input$target], by = list(var = selected[, as.character(input$groups)]), length)
			colnames(tmp) = c(as.character(subset(variables, colname == input$groups)$label), 'Count')
			selected_sum = merge(selected_sum, tmp)	
			return(selected_sum)			
		}
	})
	
	output$dist_visual = renderPlot({
		selected = Selected_group()	
		if (nrow(selected) > 0){			
			boxplot(selected[, as.character(input$target)] ~ selected[, as.character(input$groups)], outline = FALSE, col='lightgrey')
		}
	})
	output$dist_summary  = renderTable(selected_summary())
}

