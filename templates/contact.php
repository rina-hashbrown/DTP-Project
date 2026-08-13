<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Page Title -->
    <title>Any Questions?</title>
    
    <!-- Viewport Configuration: Ensures responsive layout across mobile and desktop -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <!-- External Framework: Imports W3.CSS for form field styling and grid alignment -->
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/5/w3.css">

    <!-- Embedded CSS: Styles inline validation error messages in red -->
    <style>
      .error { color: #FF0000; }
    </style>
</head>
<body>   

    <!-- 
      DEVELOPER NOTE: TRANSITION FROM PHP TO PYTHON / FLASK
      Background:
      This PHP code served as the original foundation for processing, validating, and 
      displaying the form submission results in real time.

      Migration Reason:
      During development, the web application was migrated to Python using the Flask 
      microframework. Because Flask relies on WSGI / Jinja2 templating and Python backend 
      routes—which are incompatible with embedded server-side PHP execution—this PHP 
      processing logic was translated into Python route handlers (app.py), and the HTML 
      interface was converted to Jinja2 template syntax ({% ... %}).
    -->

    <?php
    /* 
      SERVER BACKEND PROCESSING & VALIDATION (PHP)
    */

    // 1. INITIALIZE VARIABLES: Define error string buffers and form value variables
    $firstNameErr = $lastNameErr = $emailErr = $commentErr = "";
    $firstname = $lastname = $email = $comment = "";

    // 2. CHECK REQUEST METHOD: Only execute validation when form is submitted via POST
    if ($_SERVER["REQUEST_METHOD"] == "POST") {

      // --- FIRST NAME VALIDATION ---
      if (empty($_POST["first_name"])) {
        $firstNameErr = "First Name is required";
      } else {
        $firstname = test_input($_POST["first_name"]);
        // Regex Check: Ensure input contains only letters, hyphens, single quotes, and spaces
        if (!preg_match("/^[a-zA-Z\-' ]*$/", $firstname)) {
          $firstNameErr = "Only letters and white space allowed";
        }
      }

      // --- LAST NAME VALIDATION ---
      if (empty($_POST["last_name"])) {
        $lastNameErr = "Last Name is required";
      } else {
        $lastname = test_input($_POST["last_name"]);
        // Regex Check: Ensure input contains only letters, hyphens, single quotes, and spaces
        if (!preg_match("/^[a-zA-Z\-' ]*$/", $lastname)) {
          $lastNameErr = "Only letters and white space allowed";
        }
      }

      // --- EMAIL VALIDATION ---
      if (empty($_POST["email"])) {
        $emailErr = "Email is required";
      } else {
        $email = test_input($_POST["email"]);
        // Native PHP Filter Check: Validate standard email format (e.g., user@domain.com)
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
          $emailErr = "Invalid email format";
        }
      }

      // --- COMMENT VALIDATION ---
      if (empty($_POST["comment"])) {
        $commentErr = "Comment is required";
      } else {
        $comment = test_input($_POST["comment"]);
      }
    }

    /*
      test_input($data)
      --------------------------------------------------
      Purpose: Sanitizes form input to prevent XSS (Cross-Site Scripting) 
               and SQL/script injection attacks.
      Returns: Cleaned string data.
    */
    function test_input($data) {
      $data = trim($data);            // Strips unnecessary whitespace/newlines
      $data = stripslashes($data);      // Removes backslashes (\)
      $data = htmlspecialchars($data);  // Converts special characters to HTML entities
      return $data;
    }
    ?>

    <h2>Questions</h2>
    <p><span class="error">* required field</span></p>

    <!-- 
      FORM CONTAINER:
      Submits form to itself via PHP_SELF sanitized by htmlspecialchars() 
      to prevent self-XSS script injection via URL path.
    -->
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" class="form w3-container"> 

      <!-- FIRST NAME FIELD -->
      <div class="w3-row w3-section">
        <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
        <div class="w3-rest">
          Name: 
          <!-- Values are echoed back so input stays filled if validation fails -->
          <input class="w3-input w3-border" name="first_name" type="text" placeholder="First Name" value="<?php echo $firstname;?>">
          <span class="error">* <?php echo $firstNameErr;?></span>
        </div>
      </div>

      <!-- LAST NAME FIELD -->
      <div class="w3-row w3-section">
        <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
        <div class="w3-rest">
          Last Name: 
          <input class="w3-input w3-border" type="text" name="last_name" placeholder="Last Name" value="<?php echo $lastname;?>">
          <span class="error">* <?php echo $lastNameErr;?></span>
        </div>
      </div>

      <!-- EMAIL FIELD -->
      <div class="w3-row w3-section">
        <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
        <div class="w3-rest">
          Email: 
          <input class="w3-input w3-border" type="text" name="email" placeholder="Email" value="<?php echo $email;?>">
          <span class="error">* <?php echo $emailErr;?></span>
        </div>
      </div>

      <!-- COMMENT FIELD -->
      <div class="w3-row w3-section">
        <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
        <div class="w3-rest">
          Comment: 
          <textarea name="comment" rows="5" cols="40"><?php echo $comment;?></textarea>
          <span class="error"><?php echo $commentErr;?></span>
        </div>
      </div>

      <!-- SUBMIT BUTTON -->
      <input type="submit" name="submit" value="Submit">   
    </form>

    <?php
    /*
      OUTPUT DISPLAY SECTION
      --------------------------------------------------
      Renders the submitted, sanitized values directly onto the page.
    */
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
      echo "<h2>Your Input:</h2>";
      echo $firstname . "<br>";
      echo $lastname . "<br>";
      echo $email . "<br>";
      echo $comment . "<br>";
    }
    ?>

</body>
</html>