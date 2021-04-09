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
	# START CODE: (hint: using <reactive> to generate table)      #
	output$descriptive_table = ###### YOUR CODE HERE #####
	# END CODE                                                    #
	###############################################################

	#############################################################
	# Visualize univariate distributions:                       #
	#   * Frequency table barplot for categorical variables     #
	#   * Histogram for numerical variables                     #
	#   * Assign the renderPlot to [output$descriptive_visual]  #
  #                                                           #
	# START CODE: (hint: use <renderPlot> to generate plot)     #
	output$descriptive_visual = ###### YOUR CODE HERE #####
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

