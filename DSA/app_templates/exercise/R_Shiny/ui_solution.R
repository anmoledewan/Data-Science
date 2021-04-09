sidebar <- dashboardSidebar(
  width = 300,
  hr(),
  sidebarMenu(
    id="tabs",
    menuItem(
      "Exploratory", icon = icon("bullseye"), startExpanded = TRUE, 
      #######################################################
      # Create a menuSubItem, using tabName="descriptive"   #
      # START CODE                                          #
      menuSubItem("Descriptive Statistics", tabName = "descriptive", icon=icon("check")),
      # END CODE                                            #
      #######################################################
      menuSubItem("Distribution", tabName = "distribution", icon=icon("check"))
    ),
    menuItem("About", tabName="about", icon=icon("question-circle"))
  ) 
)

body <- dashboardBody(
  tabItems(
    tabItem(
      # This tabName corresponds to the tabName you set up above
      tabName = 'descriptive',  
  		fluidRow(
  		  column(
  		    width=3,
  		    selectInput(
  		      inputId = "vars",
  		      label = "Variables", 
  		      choices = structure(as.character(variables$colname[-1]), names=as.character(variables$label[-1])),
  		      multiple = FALSE
  		    )
  		  )
      ),
  		fluidRow(
  			column(
  			  width=6,
  				box(width=NULL, collapsible=TRUE, tableOutput('descriptive_table'))
        ),
  			column(
  			  width=6,
  				box(width = NULL, plotOutput('descriptive_visual'))
        )
  		)
    ),
    
    # In this [distribution] tab, complete the exercises following [descriptive] tab
    tabItem(
      tabName = "distribution",
      fluidRow(    		
        column(
          3, 
          #######################################################################
          # Create a dropdown list with choices to be all categorical variables #
          # START CODE HERE                                                     #
          selectInput(
            inputId="groups", 
            label="Groups", 
            choices=structure(
              as.character(subset(variables, type == 'categorical')$colname), 
              names = as.character(subset(variables, type == 'categorical')$label)
            ), 
            multiple=FALSE, selectize=TRUE)
          ), 
         # END CODE HERE                                                        #
         ########################################################################
      	column(6, uiOutput("select_group")),
      	column(
      	  3, 
      	  selectInput(
      	    inputId="target", 
      	    label="Variables", 
      	    choices=structure(
      	      as.character(subset(variables, type == 'numeric')$colname), 
      	      names = as.character(subset(variables, type == 'numeric')$label)
      	    ), 
      	    multiple=FALSE, selectize=TRUE))
  		), 
  		fluidRow(
  		  #######################################################
  		  # Create a tableOutput called "dist_summary"          #
  		  # START CODE                                          #
  			column(
  			  width=6,
  				box(width=NULL, tableOutput('dist_summary'))
        ),
  			# END CODE                                            #
  			#######################################################
  			
  			#######################################################
  			# Create a plotOutput called "dist_visual"            #
  			# START CODE                                          #
  			column(
  			  width=6,
  				box(width = NULL, plotOutput('dist_visual'))
        )
  			# END CODE                                            #
  			#######################################################
      )
    ),
    tabItem(tabName = "about", includeHTML("www/about.html")) 
  )
)

dbHeader = dashboardHeader(
  title = "Data Science Academy", titleWidth = 300, 
  tags$li(a(img(src = 'spg_logo.png', height = "30px"), style = "padding-top:10px; padding-bottom:10px;"), class = "dropdown")
)

dashboardPage(
  skin = "black", 
  dbHeader,
  sidebar,
  body
)


