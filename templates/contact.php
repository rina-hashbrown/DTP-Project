<!DOCTYPE html>
<html lang="en">
<head>
    <title>Any Questions?</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://www.w3schools.com/w3css/5/w3.css">

    <style>
    .error {color: #FF0000;}
    </style>
</head>
    <body>  

    <?php
    // define variables and set to empty values
    $firstNameErr = $lastNameErr = $emailErr = "";
    $firstname = $lastname = $email = $comment = "";

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
      if (empty($_POST["first_name"])) {
        $firstNameErr = "First Name is required";
      } else {
        $firstName = test_input($_POST["first_name"]);
        // check if name only contains letters and whitespace
        if (!preg_match("/^[a-zA-Z\-' ]*$/", $firstName)) {
          $firstNameErr = "Only letters and white space allowed";
        }
      }
    }

    if (empty($_POST["last_name"])) {
        $lastNameErr = "Last Name is required";
      } else {
        $lastName = test_input($_POST["last_name"]);
        // check if name only contains letters and whitespace
        if (!preg_match("/^[a-zA-Z\-' ]*$/", $lastName)) {
          $lastNameErr = "Only letters and white space allowed";
        }
      }

      if (empty($_POST["email"])) {
        $emailErr = "Email is required";
      } else {
        $email = test_input($_POST["email"]);
        // check if e-mail address is well-formed
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
          $emailErr = "Invalid email format";
        }
      }

      if (empty($_POST["comment"])) {
        $comment = "Comment is required";
    } else {
        $comment = test_input($_POST["comment"]);
          $commentErr = ("Comment invalid");
        }

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}
?>

<h2>Questions</h2>
<p><span class="error">* required field</span></p>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" class="form w3-container"> 

<div class="w3-row w3-section">
  <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
    <div class="w3-rest">
    Name: <input class="w3-input w3-border" name="first_name" type="text" placeholder="First Name" value="<?php echo $firstname;?>">
    <span class="error">* <?php echo $firstNameErr;?></span>
  </div>
</div>

<div class="w3-row w3-section">
  <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
  <div class="w3-rest">
  Last Name: <input class="w3-input w3-border" type="text" name="last_name" placeholder="Last Name" value="<?php echo $lastname;?>">
  <span class="error">* <?php echo $lastNameErr;?></span>
  </div>
</div>

<div class="w3-row w3-section">
  <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
  <div class="w3-rest">
  Email: <input class="w3-input w3-border" type="text" name="email" placeholder="Email" value="<?php echo $email;?>">
  <span class="error">* <?php echo $emailErr;?></span>
</div>

<div class="w3-row w3-section">
  <div class="w3-col" style="width:50px"><i class="w3-user xxlarge fa fa-user"></i></div>
  <div class="w3-rest">
  Comment: <textarea name="comment" rows="5" cols="40"><?php echo $comment;?></textarea>
  </div>
</div>

  <input type="submit" name="submit" value="Submit">  
</form>

<?php
echo "<h2>Your Input:</h2>";
echo $firstname;
echo "<br>";
echo $lastname;
echo "<br>";
echo $email;
echo "<br>";
echo $comment;
?>

    </form>

    </body>
    </html> 