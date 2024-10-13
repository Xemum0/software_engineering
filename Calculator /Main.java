public class Main {
    public static void main(String[] args) {
        if (args.length != 3) {
            System.out.println("error in the arguments ");
            System.out.println("Example: java test add 10.5 5.5");
            return;
        }
        
        String operation = args[0];
        Double A, B;
        
        try {
            A = Double.parseDouble(args[1]);
            B = Double.parseDouble(args[2]);
        } catch (NumberFormatException e) {
            System.out.println("Error: A and B must be valid numbers.");
            return;
        }
        
        switch (operation.toLowerCase()) {
            case "add":
                Add addOperation = new Add();
                Double result = addOperation.compute(A, B);
                System.out.println("Result: " + result);
                break;
                case "minus":
                Minus op1 = new Minus();
                Double result1 = op1.compute(A, B);
                System.out.println("Result: " + result1);
                break;
                case "div":
                Division op2 = new Division();
                Double result2 = op2.compute(A, B);
                System.out.println("Result: " + result2);
                break;
                case "mul":
                Multiplication op3 = new Multiplication();
                Double result3 = op3.compute(A, B);
                System.out.println("Result: " + result3);
                break;      
                    default:
                System.out.println("Error: Unsupported operation. Only 'add' is supported.");
                break;
        }
    }
}
