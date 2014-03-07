<!DOCTYPE html>
<html>
    <head>
        <title>Testing login</title>
    </head>
    <body>
        <form>
            <table>
                <tr>
                    <td>Username</td>
                    <td><input type="text" name="username" id="username"></td>
                </tr>
                <tr>
                    <td>Password</td>
                    <td><input type="text" name="password" id="password"></td>
                </tr>
                <tr>
                    <td></td>
                    <td><button name="submit" onclick="validate()">Login</button>
                    <button type="reset" value="reset">Reset</button></td>
                </tr>
            </table>
        </form>
    </body>
    <script>
        function validate() {
            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;
            console.log (username);
            console.log (password);
        }
    </script>
</html>