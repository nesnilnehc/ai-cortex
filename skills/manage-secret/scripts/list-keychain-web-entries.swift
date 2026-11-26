import Foundation
import Security

enum WebsiteListingError: Error {
    case usage
    case lookup(OSStatus)
    case invalidAttributes
}

func isWebsiteService(_ service: String) -> Bool {
    service.range(of: #"\A[a-z0-9]+(?:-[a-z0-9]+)*-(?:prod|dev|test|staging|local|na)-web\z"#,
                  options: .regularExpression) != nil
}

func listWebMetadata(
    arguments: [String],
    match: (CFDictionary, UnsafeMutablePointer<CFTypeRef?>?) -> OSStatus = SecItemCopyMatching
) throws -> [String] {
    let service: String?
    if arguments == ["sites"] {
        service = nil
    } else if arguments.count == 2, arguments[0] == "accounts", isWebsiteService(arguments[1]) {
        service = arguments[1]
    } else {
        throw WebsiteListingError.usage
    }

    var query: [CFString: Any] = [
        kSecClass: kSecClassGenericPassword,
        kSecReturnAttributes: true,
        kSecMatchLimit: kSecMatchLimitAll,
    ]
    if let service = service { query[kSecAttrService] = service }

    var result: CFTypeRef?
    let status = match(query as CFDictionary, &result)
    if status == errSecItemNotFound { return [] }
    guard status == errSecSuccess else { throw WebsiteListingError.lookup(status) }
    guard let items = result as? [[String: Any]] else { throw WebsiteListingError.invalidAttributes }

    let names: [String] = items.compactMap { item in
        guard let itemService = item[kSecAttrService as String] as? String else { return nil }
        if let service = service {
            guard itemService == service, let account = item[kSecAttrAccount as String] as? String,
                  !account.isEmpty else { return nil }
            return account
        }
        return isWebsiteService(itemService) ? itemService : nil
    }

    // Distinct account spellings can compare equal as Swift Strings.
    return Set(names.map { Data($0.utf8) })
        .sorted { $0.lexicographicallyPrecedes($1) }
        .map { String(decoding: $0, as: UTF8.self) }
}

#if !MANAGE_SECRET_TEST
do {
    let names = try listWebMetadata(arguments: Array(CommandLine.arguments.dropFirst()))
    var output = try JSONEncoder().encode(names)
    output.append(0x0a)
    FileHandle.standardOutput.write(output)
} catch {
    let message: String
    var status: Int32 = 1
    switch error {
    case WebsiteListingError.usage:
        message = "Usage: list-keychain-web-entries.swift sites | accounts <website-service>"
        status = 2
    case WebsiteListingError.lookup(let keychainStatus):
        message = "Could not list Keychain item attributes (OSStatus \(keychainStatus))."
    default:
        message = "Could not read Keychain website metadata."
    }
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(status)
}
#endif
