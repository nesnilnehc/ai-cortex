import Foundation
import Security

// Append this fixture to list-keychain-web-entries.swift in a temporary file,
// then run that file with xcrun swift -D MANAGE_SECRET_TEST on macOS.
let site = "customer-portal-prod-web"
let otherSite = "customer-portal-test-web"
let username = "reader\nwith line break"
let composed = "caf\u{E9}"
let decomposed = "cafe\u{301}"
let rows: [[String: Any]] = [
    [kSecAttrService as String: site, kSecAttrAccount as String: username, kSecValueData as String: Data([42])],
    [kSecAttrService as String: site, kSecAttrAccount as String: username],
    [kSecAttrService as String: site, kSecAttrAccount as String: composed],
    [kSecAttrService as String: site, kSecAttrAccount as String: decomposed],
    [kSecAttrService as String: otherSite, kSecAttrAccount as String: "other-account"],
    [kSecAttrService as String: "customer-portal-test-api", kSecAttrAccount as String: "token"],
    [kSecAttrService as String: "unrelated-web", kSecAttrAccount as String: "hidden-account"],
    [kSecAttrService as String: "customer-local-web\n", kSecAttrAccount as String: "hidden-account"],
    [kSecAttrAccount as String: "missing-site"],
]

func listFixture(_ arguments: [String], service: String?) throws -> [String] {
    try listWebMetadata(arguments: arguments) { query, result in
        let fields = query as NSDictionary
        precondition(fields[kSecClass] as? String == kSecClassGenericPassword as String)
        precondition(fields[kSecReturnAttributes] as? Bool == true)
        precondition(fields[kSecMatchLimit] as? String == kSecMatchLimitAll as String)
        precondition(fields[kSecReturnData] == nil && fields[kSecValueData] == nil)
        precondition(fields[kSecAttrService] as? String == service)
        result?.pointee = rows as CFArray
        return errSecSuccess
    }
}

let sites = try listFixture(["sites"], service: nil)
precondition(sites == [site, otherSite], "Site listing exposed an account or an unrelated service")
let accounts = try listFixture(["accounts", site], service: site)
precondition(accounts.map { Data($0.utf8) } == [decomposed, composed, username].map { Data($0.utf8) },
             "Account listing changed identities or included an account from another site")

let empty = try listWebMetadata(arguments: ["sites"]) { _, _ in errSecItemNotFound }
precondition(empty.isEmpty, "An empty Keychain should give an empty list")

do {
    _ = try listWebMetadata(arguments: ["accounts", "customer-portal-test-api"]) { _, _ in
        preconditionFailure("Invalid service reached Keychain")
    }
    preconditionFailure("Invalid service returned success")
} catch WebsiteListingError.usage {}

do {
    _ = try listWebMetadata(arguments: ["sites"]) { _, _ in errSecInteractionNotAllowed }
    preconditionFailure("Keychain rejection returned success")
} catch WebsiteListingError.lookup(let status) {
    precondition(status == errSecInteractionNotAllowed)
}

do {
    _ = try listWebMetadata(arguments: ["sites"]) { _, result in
        result?.pointee = Data([42]) as CFData
        return errSecSuccess
    }
    preconditionFailure("Unexpected Keychain response returned success")
} catch WebsiteListingError.invalidAttributes {}

print("Passed 6 website listing checks with synthetic Keychain attributes.")
